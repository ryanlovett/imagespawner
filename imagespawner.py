from dockerspawner import DockerSpawner
from traitlets import default, Unicode, List
from tornado import gen

class DockerImageChooserSpawner(DockerSpawner):
    '''Enable the user to select the docker image that gets spawned.
    
    Define the available docker images in the JupyterHub configuration and pull
    them to the execution nodes:

    c.JupyterHub.spawner_class = DockerImageChooserSpawner
    c.DockerImageChooserSpawner.dockerimages = [
        'jupyterhub/singleuser',
        'jupyter/r-singleuser'
    ]
    '''
    
    dockerimages = List(
        trait = Unicode(),
        default_value = ['jupyterhub/singleuser'],
        minlen = 1,
        config = True,
        help = "Docker images that have been pre-pulled to the execution host."
    )
    form_template = Unicode("""
        <label for="dockerimage">Select a Docker image:</label>
        <select class="form-control" name="dockerimage" required autofocus>
            {option_template}
        </select>""",
        config = True, help = "Form template."
    )
    option_template = Unicode("""
        <option value="{image}">{image}</option>""",
        config = True, help = "Template for html form options."
    )

    @default('options_form')
    def _options_form(self):
        """Return the form with the drop-down menu."""
        options = ''.join([
            self.option_template.format(image=di) for di in self.dockerimages
        ])
        return self.form_template.format(option_template=options)

    def options_from_form(self, formdata):
        """Parse the submitted form data and turn it into the correct
           structures for self.user_options."""

        default = self.dockerimages[0]

        # formdata looks like {'dockerimage': ['jupyterhub/singleuser']}"""
        dockerimage = formdata.get('dockerimage', [default])[0]

        # Don't allow users to input their own images
        if dockerimage not in self.dockerimages: dockerimage = default

        # container_prefix: The prefix of the user's container name is inherited 
        # from DockerSpawner and it defaults to "jupyter". Since a single user may launch different containers
        # (even though not simultaneously), they should have different
        # prefixes. Otherwise docker will only save one container per user. We
        # borrow the image name for the prefix.
        options = {
            'container_image': dockerimage,
            'container_prefix': '{}-{}'.format(
                super().container_prefix, dockerimage.replace('/', '-')
            )
        }
        return options

    @gen.coroutine
    def start(self, image=None, extra_create_kwargs=None,
            extra_start_kwargs=None, extra_host_config=None):
        # container_prefix is used to construct container_name
        self.container_prefix = self.user_options['container_prefix']

        # start the container
        yield DockerSpawner.start(
            self, image=self.user_options['container_image'],
            extra_create_kwargs=extra_create_kwargs,
            extra_host_config=extra_host_config)
    
# http://jupyter.readthedocs.io/en/latest/development_guide/coding_style.html
# vim: set ai et ts=4 sw=4:
