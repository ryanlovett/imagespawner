# imagespawner
DockerSpawner with image selection

Let JupyterHub users choose which docker image they want to spawn.

In your JupyterHub configuration:

```
c.JupyterHub.spawner_class = DockerImageChooserSpawner

# The admin must pull these before they can be used.
c.DockerImageChooserSpawner.dockerimages = [
	'jupyterhub/singleuser',
	'jupyter/r-singleuser'
]
```
