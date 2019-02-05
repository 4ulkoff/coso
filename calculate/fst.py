






from django.forms.models import inlineformset_factory, BaseInlineFormSet
from django.forms.formsets import DELETION_FIELD_NAME, TOTAL_FORM_COUNT
from django.forms import formsets
from django.core.exceptions import ObjectDoesNotExist


### Формсет подходов ###
class BaseTrainingExerciseSetFormset(BaseInlineFormSet):

    def should_delete(self, form):
        if self.can_delete:
            raw_delete_value = form._raw_value(DELETION_FIELD_NAME)
            should_delete = form.fields[DELETION_FIELD_NAME].clean(raw_delete_value)
            return should_delete

    def save_existing(self, form, instance, commit=True):
        """Сохраняет существующую модель."""
        setattr(form.instance, self._pk_field.name, getattr(instance, instance._meta.pk.attname))
        return super(BaseTrainingExerciseSetFormset, self).save_existing(form, instance, commit=commit)

    def _get_initial_forms(self):
        """Возвращает все начальные формы"""
        return [form for form in self.forms if
                form.instance.training_exercise_id is not None and hasattr(form, 'cleaned_data') and form.cleaned_data[
                    self._pk_field.name] is not None]

    initial_forms = property(_get_initial_forms)

    def _get_extra_forms(self):
        """Возвращает все добавленные формы"""
        return [form for form in self.forms if form.instance.training_exercise_id is None]

    extra_forms = property(_get_extra_forms)


def getTrainingExerciseSetFormset(extra=1):
    return inlineformset_factory(TrainingExercise, TrainingExerciseSet, formset=BaseTrainingExerciseSetFormset,
                                 extra=extra)


### Формсет тренировок ###
class BaseTrainingExerciseFormset(BaseInlineFormSet):
    # Использовать для вложенного формсета данные, переданные POST-ом (по умолчанию всем можно)
    _nested_allow_using_data = {}
    # для каждого вложенного формсета определяет кол-во пустых форм для отображения (для создания тренировки по шаблону)
    _nested_extras = {}
    # начальные данные для заполнения форм
    _initials = []

    def _construct_form(self, i, **kwargs):
        """
        Переопределяем, чтобы поменять параметр empty_permitted, и для задания начальных значений полей упражнений
        """
        try:
            kwargs['initial'] = self._initials[i]
        except IndexError:
            pass
        form = super(BaseInlineFormSet, self)._construct_form(i, **kwargs)
        form.empty_permitted = False
        return form

    def add_fields(self, form, index):
        # надкласс создаёт поля как обычно
        super(BaseTrainingExerciseFormset, self).add_fields(form, index)

        # создание вложенного формсета
        try:
            instance = self.get_queryset()[index]
            pk_value = instance.pk
        except IndexError:
            instance = None
            pk_value = hash(form.prefix)
        # при создании упражнения по шаблону необходимо вывести заданное в шаблоне количество форм для подходов
        extra = self._nested_extras.get(index, 1)
        # использовать для вложенного формсета данные, переданные POST-ом.
        # нужно запретить при добавлении упражнения, чтобы не было ошибок, связанных с отсутствием management_form для вложенного формсета
        allow_using_data = self._nested_allow_using_data.get(index, True)

        # кладём вложенный формсет в свойство nested
        form.nested = getTrainingExerciseSetFormset(extra)(
            data=self.data if allow_using_data else None,
            instance=instance,
            prefix='sets_%s' % pk_value
        )

    def is_valid(self):
        result = super(BaseTrainingExerciseFormset, self).is_valid()
        for form in self.forms:
            if hasattr(form, 'nested'):
                # проверяем на валидность каждую вложенную форму
                result = result and form.nested.is_valid()
        return result

    def clean(self):
        """Нужен для проверки хотя бы одного упражнения в тренировке и хотя бы одного подхода в каждом упражнении"""
        super(BaseTrainingExerciseFormset, self).clean()
        count_valid_forms = 0
        for form in self.forms:
            if not self.should_delete(form):
                count_valid_nested_forms = 0
                try:
                    if form.cleaned_data:
                        count_valid_forms += 1
                except AttributeError:
                    pass
                if hasattr(form, 'nested') and form.nested.forms:
                    for nested_form in form.nested.forms:
                        if nested_form.errors:
                            break
                        try:
                            if nested_form.cleaned_data and not form.nested.should_delete(nested_form):
                                count_valid_nested_forms += 1
                                break
                        except AttributeError:
                            # если вложенная форма не валидна, Django возбуждает
                            # исключение AttributeError для cleaned_data
                            pass
                        if not nested_form.errors and count_valid_nested_forms < 1:
                            raise forms.ValidationError('в каждом упражнении должен быть хотя бы один подход')
                else:
                    raise forms.ValidationError('в каждом упражнении должен быть хотя бы один подход')
        if count_valid_forms < 1:
            raise forms.ValidationError('в тренировке должно быть хотя бы одно упражнение')

    def save_all(self, commit=True):
        """Сохранение всех формсетов с вложенными формсетами."""
        # Сохраняем без коммита, чтобы получить self.saved_forms
        # для доступа к вложенным формсетам
        objects = self.save(commit=False)
        # Сохраняем модели, если commit=True
        if commit:
            for o in objects:
                o.save()
        # сохраняем поля многие-ко-многим
        if not commit:
            self.save_m2m()
        # сохраняем вложенные формы
        for form in set(self.initial_forms + self.saved_forms):
            if self.should_delete(form):
                continue
            form.nested.save(commit=commit)

    def save_new(self, form, commit=True):
        """Создаёт модель по данным формы и возвращает её."""
        instance = super(BaseTrainingExerciseFormset, self).save_new(form, commit=commit)
        # обновляем ссылку на объект формы
        form.instance = instance
        # обновляем ссылку у вложенных форм
        form.nested.instance = instance
        # проходимся по cleaned_data вложенных формсетов и обновляем ссылку в foreignkey
        for cd in form.nested.cleaned_data:
            cd[form.nested.fk.name] = instance
        return instance

    def save_existing(self, form, instance, commit=True):
        """Изменяет существующую модель."""
        setattr(form.instance, self._pk_field.name, getattr(instance, instance._meta.pk.attname))
        return super(BaseTrainingExerciseFormset, self).save_existing(form, instance, commit=commit)

    def total_form_count(self):
        """Переопределяем, чтобы учесть самописные initials"""
        if self.data or self.files:
            return self.management_form.cleaned_data[TOTAL_FORM_COUNT] + self.extra
        try:
            initials_len = len(self._initials)
        except TypeError:
            initials_len = 0
        return initials_len + self.initial_form_count() + self.extra

    def should_delete(self, form):
        """Определяет по данным формы, нужно ли её удалять"""

        if self.can_delete:
            raw_delete_value = form._raw_value(DELETION_FIELD_NAME)
            should_delete = form.fields[DELETION_FIELD_NAME].clean(raw_delete_value)
            return should_delete

        return False

    def _get_initial_forms(self):
        """Возвращает список всех начальных форм формсета."""
        return [form for form in self.forms if
                form.instance.training_id is not None and hasattr(form, 'cleaned_data') and form.cleaned_data[
                    self._pk_field.name] is not None]

    initial_forms = property(_get_initial_forms)

    def _get_extra_forms(self):
        """Возвращает список всех добавленных форм формсета."""
        return [form for form in self.forms if
                form.instance.training_id is None or not hasattr(form, 'cleaned_data') or (
                            hasattr(form, 'cleaned_data') and form.cleaned_data[self._pk_field.name] is None)]

    extra_forms = property(_get_extra_forms)

    @classmethod
    def set_nested_extras(cls, nested_extras):
        """Костыль для задания кол-ва пустых вложенных форм для каждой формы"""
        cls._nested_extras = nested_extras

    @classmethod
    def set_initials(cls, initials):
        """Костыль для задания начальных данных форм"""
        cls._initials = initials

    @classmethod
    def set_nested_allow_using_data(cls, nested_allow_using_data):
        """Костыль для запрета использования данных POST-а при сохранении некоторых вложенных форм"""
        cls._nested_allow_using_data = nested_allow_using_data


def getTrainingExerciseFormset(extra, nested_extras={}, initials=[], nested_allow_using_data={}):
    """Обёртка над inlineformset_factory для установления всех дополнительных параметров:
    количества пустых форм для ввода упражнений, количества пустых форм для ввода подходов для каждого упражнения
    и начальных данных для форм ввода упражнения"""
    BaseTrainingExerciseFormset.set_nested_extras(nested_extras)
    BaseTrainingExerciseFormset.set_initials(initials)
    BaseTrainingExerciseFormset.set_nested_allow_using_data(nested_allow_using_data)
    return inlineformset_factory(Training, TrainingExercise, formset=BaseTrainingExerciseFormset, extra=extra)


@login_required
def trainings_add(request, trainingTemplateId=None):
    """Добавление тренировки"""
    user = request.user
    try:
        trainingTemplate = TrainingTemplate.objects.get(id=int(trainingTemplateId)) if trainingTemplateId else None
    except ObjectDoesNotExist:
        trainingTemplate = None
    training = Training()

    if request.method == 'POST':
        nameForm = TrainingNameForm(request.POST, instance=training)
        formset = getTrainingExerciseFormset(extra=0)(request.POST, instance=training)
        if nameForm.is_valid() and formset.is_valid():
            nameData = nameForm.cleaned_data
            training.user = user
            training.name = nameData['name']
            training.description = nameData["description"]
            training.training_at = nameData['training_at']
            if trainingTemplate:
                training.trainingTemplate = trainingTemplate
            training.user_weight = user.get_profile().weight
            training.save()
            formset.save_all()
            return HttpResponseRedirect("/trainings/%s/card/" % training.id)
    else:
        if trainingTemplate is not None:
            trainingTemplateExercises = trainingTemplate.trainingtemplateexercise_set.order_by('position')
            training.name = trainingTemplate.name
            training.description = trainingTemplate.description
            training.user = user
            training.training_at = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
            initials = []
            for position, templateExercise in enumerate(trainingTemplateExercises):
                initials.append({
                    'exercise': templateExercise.exercise,
                    'position': templateExercise.position
                })
            nested_extras = dict((p, tE.sets) for p, tE in enumerate(trainingTemplateExercises))
            formset = getTrainingExerciseFormset(extra=0, nested_extras=nested_extras, initials=initials)(
                instance=training)
        else:
            formset = getTrainingExerciseFormset(extra=1)(instance=training)
        nameForm = TrainingNameForm(instance=training)
    return render_to_response(
        "trainings/add.html",
        {
            "training": training,
            "trainingName": nameForm,
            "exercises": formset,
            "hide_exercises": ""
        },
        context_instance=RequestContext(request)
    )


@login_required
def trainings_add_exercise(request, trainingId=None):
    """Экшн для добавления формы упражнения"""
    user = request.user
    training = Training.objects.get(id=trainingId, user=user) if trainingId is not None else Training()
    if request.method == 'POST':
        nested_allow_using_post_data = {int(request.POST.get('trainingexercise_set-TOTAL_FORMS', 0)): False}
        formset = getTrainingExerciseFormset(extra=1, nested_allow_using_data=nested_allow_using_post_data)(
            request.POST, instance=training)
    else:
        formset = getTrainingExerciseFormset(extra=1)(instance=training)
    formset.forms = formset.forms[-1:]
    return render_to_response("trainings/exercise_forms.html", {"exercises": formset},
                              context_instance=RequestContext(request))