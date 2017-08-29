#!/usr/bin/python
# -*- coding: ascii -*-
import os
import subprocess

# project to take the config from
project_path = "https://raw.githubusercontent.com/jmason-va/angular-seed/master"

# paths to generic config files
jenkinsfile = "{}/jenkinsfile".format(project_path)
tasks = "{}/tasks.py".format(project_path)
app_yaml = "{}/app.yaml".format(project_path)
angular_cli_json = "{}/.angular-cli.json".format(project_path)
styles = "{}/src/styles.scss".format(project_path)
karma = "{}/karma.conf.js".format(project_path)
readme = "{}/README.md".format(project_path)
polyfills = "{}/src/polyfills.ts".format(project_path)
# color terminal output
GREEN = '\033[92m'
RED = '\033[91m'
END = '\033[0m'


def get_file(path, filename):
  """takes a path to a github raw page and outputs a file"""
  os.system('curl {} -o "{}"'.format(path, filename))


def generate_config_files(project_name, parent_project_name):
  """generates vendasta config needed for a frontend microservice"""
  ls_output = subprocess.check_output('ls')

  print '\n{}configuring jenkinsfile{}'.format(GREEN, END)
  get_file(jenkinsfile, "jenkinsfile")  # generate a generic angular jenkinsfile
  replace_in_file('jenkinsfile', 'angular-seed', project_name)  # update the label to include the project name
  os.system('mv jenkinsfile {}'.format(project_name))  # move the jenkinsfile into the base directory

  print '\n{}configuring tasks.py{}'.format(GREEN, END)
  get_file(tasks, "tasks.py")  # generate a generic angular tasks file
  replace_in_file('tasks.py', '<base-project>',
                  parent_project_name)  # configure which application this service deploys to
  os.system('mv tasks.py {}'.format(project_name))  # move the tasks file into the base directory

  print '\n{}configuring app.yaml{}'.format(GREEN, END)
  get_file(app_yaml, "app.yaml")  # generate a generic app.yaml file
  replace_in_file('app.yaml', 'angular-seed', project_name)  # configure the service name
  os.system('mv app.yaml {}'.format(project_name))  # move the app.yaml file into the base directory

  print '\n{}configuring karma.conf{}'.format(GREEN, END)
  os.system('npm --prefix {} install --save-dev karma-phantomjs-launcher '.format(
    project_name))  # install phantomjs launcher for tests
  os.system('npm --prefix {} install --save intl'.format(project_name))  # install intl as a dep for phantomjs
  os.system('rm {}/karma.conf.js'.format(project_name))  # move the karma.conf.js file into the base directory
  get_file(karma, "karma.conf.js")
  os.system(
    'mv karma.conf.js {}/karma.conf.js'.format(project_name))  # move the karma.conf.js file into the base directory

  print '\n{}configuring polyfills{}'.format(GREEN, END)
  os.system('rm {}/src/polyfills.ts'.format(project_name))  # move the polyfills file into the src directory
  get_file(polyfills, "polyfills.ts")  # generate a generic app.yaml file
  os.system('mv polyfills.ts {}/src'.format(project_name))  # move the app.yaml file into the base directory

  print '\n{}configuring readme{}'.format(GREEN, END)
  os.system('rm {}/README.md'.format(project_name))  # remove cli readme
  get_file(readme, "README.md")  # generate basic readme
  os.system('mv README.md {}'.format(project_name))  # move basic readme into base folder

  print '\n{}adding basic styles{}'.format(GREEN, END)
  os.system('rm {}/src/styles.css'.format(project_name))  # remove styles.css file
  get_file(styles, "styles.scss")  # get basic styles
  os.system('mv styles.scss {}/src'.format(project_name))  # move styles.scss to the src

  print '\n{}updating default styling {}'.format(GREEN, END)
  replace_in_file('{}/.angular-cli.json'.format(project_name), 'css',
                  'scss')  # configure project to use scss by default
  replace_in_file('{}/.angular-cli.json'.format(project_name), 'dist',
                  'target')  # output do target folder instead of dist

  print '\n{}adding material to project{}'.format(GREEN, END)
  app_module_path = '{}/src/app/app.module.ts'.format(project_name)
  replace_in_file(app_module_path, """import { NgModule } from '@angular/core';""",  # add material import to app.module
                  """import { NgModule } from '@angular/core';
                  import { MaterialModule } from '@angular/material';
                  """)
  replace_in_file(app_module_path, 'imports: [', 'imports: [ MaterialModule,')

  print '\n{}updating package.json{}'.format(GREEN, END)
  package_json_path = '{}/package.json'.format(project_name)  # add deps to package json
  replace_in_file(package_json_path, '"dependencies": {',
                  '"dependencies": { \n    "@angular/material": "2.0.0-beta.3",')
  # os.system('npm --prefix {} install angular-material --save'.format(project_name))      # having trouble installing this properly

  # add basic app component
  clear_file('{}/src/app/app.component.html'.format(project_name),  # clear app.component
             """
  <md-card style="text-align: center; margin: 30px auto; width: 250px;">
    <img src="https://vbc-frontend.storage-download.googleapis.com/salesperson-details/vendasta_icon.png"/>
    <div>Vendasta Frontend Microservice</div>
  </md-card>
  <router-outlet></router-outlet>
             """)

  # add basic test
  clear_file('{}/src/app/app.component.spec.ts'.format(project_name),
             """
  import { TestBed, async } from '@angular/core/testing';
  import { RouterTestingModule } from '@angular/router/testing';
  
  import { AppComponent } from './app.component';
  
  describe('sanity', () => {
    it('succeeds properly', () => {
        expect(true).toBe(true);
    });
  });
             """)


def generate_angular_cli_project(project_name, parent_project_name):
  """generate a project from scratch"""
  print '\n{}generating new angular project {}{}'.format(GREEN, project_name, END)
  print '{}add routing in {} to your new microservice at https://github.com/vendasta/{}/blob/master/src/dispatch.yaml{}\n\n'.format(
    GREEN, parent_project_name, parent_project_name, END)
  os.system('ng new {} --routing'.format(project_name))


def replace_in_file(file_name, to_replace, replacement):
  # Read in the file
  with open(file_name, 'r') as file:
    filedata = file.read()
  # Replace the target string
  filedata = filedata.replace(to_replace, replacement)
  # Write the file out again
  with open(file_name, 'w') as file:
    file.write(filedata)


def clear_file(file_name, text=''):
  # Read in the file
  with open(file_name, 'r') as file:
    filedata = file.read()
  # Write the file out again with the text
  with open(file_name, 'w') as file:
    file.write(text)


def main():
  print "\nthis will generate a angular project from the standard-cli."
  print "it will also generate the Vendasta config needed for a frontend microservice."
  print "{}warning: this will fail if you do not have the angular-cli installed on your machine.\n{}".format(RED, END)

  project_name = raw_input("enter a project name: ").strip()
  parent_project_name = raw_input("enter the project that will serve this module: ").strip()

  generate_angular_cli_project(project_name, parent_project_name)

  print '\n\n\n{}generating vendasta config for {}{}'.format(GREEN, project_name, END)
  generate_config_files(project_name, parent_project_name)

  print '\n\n\n{}installing node modules{}'.format(GREEN, END)
  os.system('npm --prefix {} install'.format(project_name))

  print '\n\n\n{}starting project{}'.format(GREEN, END)
  os.system('npm --prefix {} start'.format(project_name))


main()
