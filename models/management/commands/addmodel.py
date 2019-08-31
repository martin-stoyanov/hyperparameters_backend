from django.core.management.base import BaseCommand, CommandError
from models.models import HPJS_Model, Trial, Parameter, ParameterValue

class Command(BaseCommand):
  def handle(self, *args, **options):
    # deleting previous records so we can re-run the admin-command
    HPJS_Model.objects.all().delete()
    Trial.objects.all().delete()
    Parameter.objects.all().delete()
    ParameterValue.objects.all().delete()

    self.stdout.write("adding model to database", ending='\n')

    # adding HPJS_Model
    model1 = HPJS_Model(name="Mnist")
    model1.save()
    
    # adding trial and linking it to the model
    trial1 = Trial(trial=1, start_time="2019-02-12 12:12", 
      end_time="2019-02-12 12:12", accuracy=0.3, hpjs_model=model1)

    trial1.save()

    # adding parameter value and linking it to the model
    parameter1 = Parameter(name="modelType", hpjs_model=model1)
    parameter1.save()

    # adding parameter value and linking it to the parameter and trial
    parametervalue1 = ParameterValue(value="DenseNet", trial=trial1, 
      parameter=parameter1)

    parametervalue1.save()

