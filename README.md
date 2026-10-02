# kitchen-keeper

A self-hosted Flask recipe management application.

## Deployment information

Kitchen Keeper runs as a Python 3.11 Flask application served by Gunicorn in
Docker. PostgreSQL 16 stores recipes, ingredients, and instructions. Recipe
images are stored on disk outside the app container.

| Item | Purpose |
| --- | --- |
| GitHub: `prowler0305/kitchen-keeper`, branch `main` | Stores the source code and deployment configuration |
| Docker Hub: `prowler0305/kitchen-keeper:latest` | Stores the image pulled by the NAS |
| `Dockerfile` | Packages the application and installs the pinned dependencies from `requirements.txt` |
| `docker-compose.yml` | Builds `kitchen-keeper-local` and runs the app and PostgreSQL locally |
| `docker-compose.synology.yml` | Runs the published Docker Hub image and PostgreSQL on Synology |
| Synology project | `kitchen-keeper`, located at `/volume1/docker/kitchen-keeper` |
| App container | `kitchen-keeper-app`, with host port `8000` mapped to container port `8000` |
| App URL on the home network | <http://DS224plus:8000> |

GitHub and Docker Hub are separate services. Pushing a Git commit does not
build or publish an image. Building an image does not upload it to Docker Hub.
There is currently no automated release pipeline in this repository.

The NAS uses this setting under the existing `app` service:

```yaml
  app:
    image: prowler0305/kitchen-keeper:latest
    pull_policy: always
```

`pull_policy: always` makes Compose check Docker Hub and pull the current image
when preparing the project, even if an image with the same tag is already
stored on the NAS. Starting or restarting an existing container alone does not
download a new image.

## Deployment process

### 1. Test and save the source changes

Test changes locally using PyCharm's `KitchenKeeper` run configuration. It uses
the `kitchen-keeper` Conda environment and `DevelopmentConfig`. With the local
PostgreSQL service running, the development app is available at
<http://localhost:5000>.

Review the changes, commit the intended files, and push `main` to GitHub. Use
PyCharm's Git tools or a terminal with GitHub authentication configured.

Docker builds from the current files on your computer, including uncommitted
changes. Committing first makes it easier to identify the source for a release.

### 2. Build the image locally

Start Docker Desktop. Run Docker commands from the project directory in
Windows PowerShell, or a WSL terminal with Docker Desktop integration enabled.
The project can be opened in PowerShell with:

```powershell
Set-Location '\\wsl.localhost\Ubuntu\home\prowl\dev\PycharmProjects\kitchen-keeper'
```

Build for the existing Synology deployment's `linux/amd64` platform:

```bash
docker build --platform linux/amd64 -t kitchen-keeper-local:latest -t prowler0305/kitchen-keeper:latest .
```

Both tags refer to the same image. Seeing both names in Docker Desktop's local
Images tab does not mean the image was built twice or uploaded.

Alternatively, on the current AMD64 Docker Desktop installation, build through
the local Compose file and then add the Docker Hub tag:

```bash
docker compose -f docker-compose.yml build app
docker tag kitchen-keeper-local:latest prowler0305/kitchen-keeper:latest
```

Choose one build method. Neither method starts the app container.

### 3. Push the image to Docker Hub

Sign in to Docker Hub through Docker Desktop, or run `docker login` if needed.
Then publish the image:

```bash
docker push prowler0305/kitchen-keeper:latest
```

Wait for a successful completion with a `latest: digest: sha256:...` message.
The Docker Hub repository's Tags page should show the recent update to
`latest`.

### 4. Update the existing Synology project

In Synology **Container Manager**:

1. Open **Project** and select **kitchen-keeper**.
2. Choose **Action → Stop** for the whole project. Both the app and PostgreSQL
   must stop before **Build** becomes available.
3. If the Compose configuration changed, open **YAML Configurations** and apply
   the corresponding changes from `docker-compose.synology.yml`. Confirm that
   `pull_policy: always` is under `app`, aligned with `image`.
4. Save the configuration and choose **Action → Build** if the save operation
   has not already prepared the project. Watch the operation output for the
   app image being pulled successfully.
5. Choose **Start** once the operation finishes. Check that both containers
   are running and review the app's logs if startup fails.

The NAS's project configuration is a separate copy. Editing the local Compose
file or pushing it to GitHub does not automatically update that copy.

The Synology Compose file specifies an `image`, so the NAS downloads the
packaged application. Synology's **Build** action prepares the Compose project;
it does not compile this application from source on the NAS. **Run** on the
Image page opens a new-container wizard and is not part of this project update
process.

### 5. Verify the deployed app

Open <http://DS224plus:8000> from a computer on the home network. Press
**Ctrl+Shift+R** to refresh cached JavaScript and CSS, then test the changed
behavior on the deployed app.

If the server name does not resolve, find the NAS's current IPv4 address in
**DSM → Control Panel → Network → Network Interface** and use
`http://<NAS-IP>:8000`. The server name is shown under **Network → General**.

## Storage and startup

- PostgreSQL uses the Compose named volume `postgres_data`.
- Recipe uploads use the NAS folder `/volume1/docker/kitchen-keeper/uploads`,
  mounted at `/app/uploads/recipes` in the app container.
- `start.sh` runs `flask --app run.py db upgrade` before starting Gunicorn.
  Include a migration when a change alters the database schema.
- A normal update uses **Stop → Build → Start**. **Stop** preserves containers
  and storage. Avoid using **Clean** or **Delete** as routine update actions;
  those actions remove project resources and can affect stored data.

For pull-policy behavior, see the [Docker Compose service documentation](https://docs.docker.com/reference/compose-file/services/#pull_policy).
For the project actions, see [Synology's Container Manager documentation](https://kb.synology.com/en-global/DSM/help/ContainerManager/docker_project).
