from contentctl.actions.initialize import Initialize
import tyro
from contentctl.objects.config import Config_Base, CustomApp, init, validate, build,  new, deploy_acs, deploy_rest, test, test_servers, inspect, allapps
from typing import Union
from contentctl.actions.validate import Validate
from contentctl.actions.new_content import NewContent
from contentctl.actions.detection_testing.GitService import GitService
from contentctl.actions.build import (
     BuildInputDto,
     DirectorOutputDto,
     Build,
)

from contentctl.actions.test import TestInputDto

from contentctl.actions.inspect import Inspect
import sys
import warnings
import pathlib
from contentctl.input.yml_reader import YmlReader

# def print_ascii_art():
#     print(
#         """
# Running Splunk Security Content Control Tool (contentctl) 
# ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
# ⠀⠀⠀⠀⠀⠀⠀⠀⠀⢶⠛⡇⠀⠀⠀⠀⠀⠀⣠⣦⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
# ⠀⠀⠀⠀⠀⠀⠀⠀⣀⠼⠖⠛⠋⠉⠉⠓⠢⣴⡻⣾⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
# ⠀⠀⠀⢀⡠⠔⠊⠁⠀⠀⠀⠀⠀⠀⣠⣤⣄⠻⠟⣏⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
# ⠀⣠⠞⠁⠀⠀⠀⡄⠀⠀⠀⠀⠀⠀⢻⣿⣿⠀⢀⠘⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
# ⢸⡇⠀⠀⠀⡠⠊⠀⠀⠀⠀⠀⠀⠀⠀⠉⠉⠀⠈⠁⠘⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
# ⢸⡉⠓⠒⠊⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⢄⠀⠀⠀⠈⢦⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
# ⠈⡇⠀⢠⠀⠀⠀⠀⠀⠀⠀⠈⡷⣄⠀⠀⢀⠈⠀⠀⠑⢄⠀⠑⢄⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
# ⠀⠹⡄⠘⡄⠀⠀⠀⠀⢀⡠⠊⠀⠙⠀⠀⠈⢣⠀⠀⠀⢀⠀⠀⠀⠉⠒⠤⣀⠀⠀⠀⠀⠀⠀⠀⠀
# ⠀⠀⠉⠁⠛⠲⢶⡒⠈⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⡄⠀⠀⠉⠂⠀⠀⠀⠀⠤⡙⠢⣄⠀⠀⠀⠀⠀
# ⠀⠀⠀⠀⠀⠀⠀⢹⠀⠀⡀⠀⠀⢸⠀⠀⠀⠀⠘⠇⠀⠀⠀⠀⠀⠀⠀⠀⢀⠈⠀⠈⠳⡄⠀⠀⠀
# ⠀⠀⠀⠀⠀⠀⠀⠈⡇⠀⠣⠀⠀⠈⠀⢀⠀⠀⠀⠀⠀⠀⢀⣀⠀⠀⢀⡀⠀⠑⠄⠈⠣⡘⢆⠀⠀
# ⠀⠀⠀⠀⠀⠀⠀⠀⢧⠀⠀⠀⠀⠀⠀⠿⠀⠀⠀⠀⣠⠞⠉⠀⠀⠀⠀⠙⢆⠀⠀⡀⠀⠁⠈⢇⠀
# ⠀⠀⠀⠀⠀⠀⠀⠀⢹⠀⢤⠀⠀⠀⠀⠀⠀⠀⠀⢰⠁⠀⠀⠀⠀⠀⠀⠀⠀⠁⠀⠙⡄⠀⡀⠈⡆
# ⠀⠀⠀⠀⠀⠀⠀⠀⠸⡆⠘⠃⠀⠀⠀⢀⡄⠀⠀⡇⠀⠀⡄⠀⠀⠀⠰⡀⠀⠀⡄⠀⠉⠀⠃⠀⢱
# ⠀⠀⠀⠀⠀⠀⠀⠀⠀⢣⡀⠀⠀⡆⠀⠸⠇⠀⠀⢳⠀⠀⠈⠀⠀⠀⠐⠓⠀⠀⢸⡄⠀⠀⠀⡀⢸
# ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢳⡀⠀⢻⠀⠀⠀⠀⢰⠛⢆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠃⠀⡆⠀⠃⡼
# ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⣷⣤⣽⣧⠀⠀⠀⡜⠀⠈⠢⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⠃
# ⠀⠀⠀⠀⠀⠀⠀⠀⠀⣾⣿⣿⣇⡿⠹⣷⣄⣬⡗⠢⣤⠖⠛⢳⣤⣀⠀⠀⠀⠀⠀⠀⠀⠀⡰⠃⠀
# ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⠋⢠⣾⢿⡏⣸⠀⠀⠈⠋⠛⠧⠤⠘⠛⠉⠙⠒⠒⠒⠒⠉⠀⠀⠀
# ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠉⠻⠶⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀

#     By: Splunk Threat Research Team [STRT] - research@splunk.com
#     """
#     )




def init_func(config:test):    
    Initialize().execute(config)


def validate_func(config:validate)->DirectorOutputDto:
    validate = Validate()
    return validate.execute(config)


def build_func(config:build)->DirectorOutputDto:
    # First, perform validation. Remember that the validate
    # configuration is actually a subset of the build configuration
    director_output_dto = validate_func(config)
    builder = Build()
    return builder.execute(BuildInputDto(director_output_dto, config))

def inspect_func(config:inspect)->str:
    builder = build_func(config)
    inspect_token = Inspect().execute(config)
    return inspect_token
    

def new_func(config:new):
    NewContent().execute(config)



def deploy_acs_func(config:deploy_acs):
    #This is a bit challenging to get to work with the default values.
    raise Exception("deploy acs not yet implemented")

def deploy_rest_func(config:deploy_rest):
    raise Exception("deploy rest not yet implemented")
    

def test_func(config:test, apps:allapps):
    director_output_dto = build_func(config)
    
    
    gitServer = GitService(director=director_output_dto,config=config)
    
    detections_to_test = gitServer.getContent()

    

    test_input_dto = TestInputDto(detections_to_test, config)
    
    t = Test()

    #t.execute(test_input_dto)

def test_servers_func(config:test_servers):
    raise Exception("Not yet done")

    

def main():
    
    
    try:
        configFile = pathlib.Path("contentctl.yml")
        if not configFile.is_file():
            t = test()
            config_obj = t.model_dump()
            #raise Exception(f"Config File {configFile} does not exist. Please create it with 'contentctl init'")        
        else:
            config_obj = YmlReader().load_file(configFile)
            t = test.model_validate(config_obj)
    except Exception as e:
        print(f"Error validating 'contentctl.yml':\n{str(e)}")
        sys.exit(1)
    
    try:
        appsFile = pathlib.Path("apps.yml")
        if not appsFile.is_file():
            print("make new file")
            apps = allapps(a=[])
            #raise Exception(f"Config File {configFile} does not exist. Please create it with 'contentctl init'")        
        else:
            apps_obj = YmlReader().load_file(appsFile,add_fields=False)
            apps = allapps.model_validate(apps_obj)

    except Exception as e:
        print(f"Error validating 'contentctl.yml':\n{str(e)}")
        sys.exit(1)
        
    
    # For ease of generating the constructor, we want to allow construction
    # of an object from default values WITHOUT requiring all fields to be declared
    # with defaults OR in the config file. As such, we construct the model rather
    # than model_validating it so that validation does not run on missing required fields.
    # Note that we HAVE model_validated the test object fields already above

    models = tyro.extras.subcommand_type_from_defaults(
        {
            "init":init.model_validate(config_obj),
            "validate": validate.model_validate(config_obj),
            "build":build.model_validate(config_obj),
            "inspect": inspect.model_construct(**t.__dict__),
            "new":new.model_validate(config_obj),
            "test":test.model_validate(config_obj),
            "test_servers":test_servers.model_validate(config_obj),
            "deploy_acs": deploy_acs.model_construct(**t.__dict__),
            #"deploy_rest":deploy_rest()
        }
    )
    

    # Since some model(s) were constructed and not model_validated, we have to catch
    # warnings again when creating the cli
    with warnings.catch_warnings(action="ignore"):
        config = tyro.cli(models)
   
    
    
    if type(config) == init:
        t.__dict__.update(config.__dict__)
        init_func(t)
    elif type(config) == validate:
        validate_func(config)
    elif type(config) == build:
        build_func(config)
    elif type(config) == new:
        new_func(config)
    elif type(config) == inspect:
        inspect_func(config)
    elif type(config) == deploy_acs:
        updated_config = deploy_acs.model_validate(config)
        deploy_acs_func(updated_config)
    elif type(config) == deploy_rest:
        deploy_rest_func(config)
    elif type(config) == test:
        test_func(config, apps)
    elif type(config) == test_servers:
        test_servers_func(config)
    else:
        raise Exception(f"Unknown command line type '{type(config).__name__}'")
    