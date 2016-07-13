from dockerspawner import DockerSpawner
from traitlets import default, Unicode, List

class DockerImageChooserSpawner(DockerSpawner):
	'''In your JupyterHub configuration:

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
		options = ''.join([
			self.option_template.format(image=di) for di in self.dockerimages
		])
		return self.form_template.format(option_template=options)

	def options_from_form(self, formdata):
		"""formdata looks like {'dockerimage': ['jupyterhub/singleuser']}"""
		default = self.dockerimages[0]
		dockerimage = formdata.get('dockerimage', [default])[0]
		if dockerimage not in self.dockerimages:
			dockerimage = default

		# The prefix of the user's container name is normally "jupyter".
		# Since a single user will launch different containers (though not
		# simultaneously), they should have different prefixes.
		# We borrow the image name for the prefix.
		self.container_prefix = dockerimage.replace('/', '-')
		self.container_image = dockerimage

		#options = { 'container': container }
		#return options
		return {}
