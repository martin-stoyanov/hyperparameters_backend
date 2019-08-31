import graphene
from graphene_django.types import DjangoObjectType
from .models import HPJS_Model, Trial, Parameter, ParameterValue

# defining return types
class ModelType(DjangoObjectType):
  class Meta:
    model = HPJS_Model

class TrialType(DjangoObjectType):
  class Meta:
    model = Trial

class ParameterType(DjangoObjectType):
  class Meta:
    model = Parameter

class ParameterValueType(DjangoObjectType):
  class Meta:
    model = ParameterValue

# defining input types
class TrialInputType(graphene.InputObjectType):
  trial = graphene.Int()
  start_time = graphene.DateTime()
  end_time = graphene.DateTime()
  accuracy = graphene.Float()

class ParameterInputType(graphene.InputObjectType):
  name = graphene.String()

class ParameterValueInputType(graphene.InputObjectType):
  value = graphene.String()
  trial = graphene.Int(required=True)
  parameter_name = graphene.String(required=True)

class ModelAddMutation(graphene.Mutation):
  class Arguments:
    # The input arguments for the mutation
    name = graphene.String(required=True)
    trials = graphene.List(TrialInputType)
    parameters = graphene.List(ParameterInputType)
    parameter_values = graphene.List(ParameterValueInputType)
    
  # The class attributes define the response of the mutation
  hpjs_model = graphene.Field(ModelType)

  def mutate(self, info, name, trials, parameters, parameter_values):
    model = HPJS_Model(name=name)
    model.save()

    for trial in trials:
      t = Trial(trial=trial.trial, start_time=trial.start_time, end_time=trial.end_time, 
        accuracy=trial.accuracy, hpjs_model=model)
      t.save()

    for parameter in parameters:
      p = Parameter(name=parameter.name, hpjs_model=model)
      p.save()

    for parameter_value in parameter_values:
      t = None
      for trial in model.trials.all():
        if trial.trial == parameter_value.trial:  
          t = trial
          break

      p = None
      for parameter in model.parameters.all():
        if parameter.name == parameter_value.parameter_name:  
          p = parameter
          break

      pv = ParameterValue(value=parameter_value.value, trial=t, parameter=p)
      pv.save()

    # Notice we return an instance of this mutation
    return ModelAddMutation(hpjs_model=model)
    #return ModelAddMutation(hpjs_model=model, trial=trial1, parameter=parameter1,
    #  parametervalue=parametervalue1)

class ModelDeleteMutation(graphene.Mutation):
  class Arguments:
    # The input arguments for this mutation
    id = graphene.Int(required=True)

  # The class attributes define the response of the mutation
  id = graphene.Int()

  def mutate(self, info, id):
    model = HPJS_Model.objects.get(id=id)
    model.delete()
    # Notice we return an instance of this mutation
    return ModelDeleteMutation(id=id)

class ModelEditMutation(graphene.Mutation):
  class Arguments:
    # The input arguments for the mutation
    id = graphene.Int(required=True)
    trials = graphene.List(TrialInputType, required=False)
    parameters = graphene.List(ParameterInputType, required=False)
    parameter_values = graphene.List(ParameterValueInputType)

  hpjs_model = graphene.Field(ModelType)

  def mutate(self, info, id, trials, parameters, parameter_values):
    model = HPJS_Model.objects.get(id=id)
    
    # deleting previous trials before adding the new ones
    previous_trials = Trial.objects.select_related('hpjs_model').all()
    previous_trials.delete()

    for trial in trials:
      t = Trial(trial=trial.trial, start_time=trial.start_time, end_time=trial.end_time, 
        accuracy=trial.accuracy, hpjs_model=model)
      t.save()

    # deleting previous parameters before adding the new ones
    previous_parameters = Parameter.objects.select_related('hpjs_model').all()
    previous_parameters.delete()

    for parameter in parameters:
      p = Parameter(name=parameter.name, hpjs_model=model)
      p.save()

    # deleting previous parameter values before adding the new ones
    previous_parameter_values = ParameterValue.objects.select_related('hpjs_model').all()
    previous_parameter_values.delete()

    for parameter_value in parameter_values:
      t = None
      for trial in model.trials.all():
        if trial.trial == parameter_value.trial:  
          t = trial
          break

      p = None
      for parameter in model.parameters.all():
        if parameter.name == parameter_value.parameter_name:  
          p = parameter
          break

      pv = ParameterValue(value=parameter_value.value, trial=t, parameter=p)
      pv.save()

    return ModelEditMutation(hpjs_model=model)

class ModelMutation:
    add_model = ModelAddMutation.Field()
    delete_model = ModelDeleteMutation.Field()
    edit_model = ModelEditMutation.Field()

class ModelQuery(object):
  model = graphene.Field(ModelType,
    id=graphene.Int(),
    name=graphene.String())

  all_models = graphene.List(ModelType)
  all_trials = graphene.List(TrialType)
  all_parameters = graphene.List(ParameterType)
  all_parameter_values = graphene.List(ParameterValueType)

  def resolve_model(self, info, **kwargs):
    id = kwargs.get('id')
    name = kwargs.get('name')
    query = HPJS_Model.objects.prefetch_related('trials').prefetch_related('parameters')

    if id is not None:
      return query.get(pk=id)

    if name is not None:
      return query.get(name=name)

    return None

  def resolve_all_models(self, info, **kwargs):
    return HPJS_Model.objects.all()

  def resolve_all_trials(self, info, **kwargs):
    return Trial.objects.select_related('hpjs_model').all()

  def resolve_all_parameters(self, info, **kwargs):
    return Parameter.objects.select_related('hpjs_model').all()

  def resolve_all_parametervalues(self, info, **kwargs):
    return ParameterValue.objects.select_related('hpjs_model').all()
