# Control de Sesiones

Bitácora del avance del proyecto (sitio web Dra. Romero Nossa), sesión por sesión. Cada vez que se trabaje en el proyecto, se agrega una entrada nueva **arriba** de las anteriores (orden cronológico inverso, la más reciente primero).

## Cómo usar este archivo

1. Al iniciar una sesión de trabajo, copia la plantilla de abajo y complétala.
2. Al terminar, marca qué quedó pendiente para la próxima sesión.
3. No borres sesiones anteriores: es el historial del proyecto.

### Plantilla

```
## [Fecha AAAA-MM-DD] - [Título corto de la sesión]

**Objetivo del día:**
-

**Hecho:**
-

**Pendiente / próximos pasos:**
-

**Notas / decisiones:**
-
```

---

## 2026-09-07 - Migración a FastAPI + Docker + CI/CD

**Objetivo del día:**
- Eliminar los formularios PHP (nunca funcionaron) y dejar el sitio listo para desplegarse en Docker como uno de tres proyectos en el VPS de Hostinger, vía CI/CD.

**Hecho:**
- Se creó la app `app/` (FastAPI): sirve el sitio estático (`www/`) y expone `POST /api/contact` y `POST /api/appointment`, que envían correo real por SMTP (stdlib `smtplib`) manteniendo el mismo contrato que ya esperaba `assets/vendor/php-email-form/validate.js` (responde texto plano `"OK"` o un mensaje de error), así que no hubo que tocar ese JS.
- Se actualizó `index.html`: los `action` de los formularios apuntan a `/api/contact` y `/api/appointment`; se corrigieron los `value` de los `<select>` de especialidad/ciudad en el formulario de cita para que coincidan con la etiqueta visible (antes decían "Department 1/2/3", "Doctor 1/2/3").
- Se borró `forms/` (PHP) y el `main.py` de scaffold en la raíz.
- Se agregaron `Dockerfile` (multi-stage, `python:3.13-slim` + `uv`, no-root, healthcheck), `.dockerignore`, `docker-compose.yml` (con las labels de Traefik para `cardiologia.futurehealthlabmx.io`) y `docker-compose.override.yml` (build local + puerto 8000 para desarrollo).
- Se agregó `.github/workflows/deploy.yml`: build + push a GHCR y despliegue por SSH al VPS en cada push a `master`.
- Se agregaron las dependencias (`fastapi`, `uvicorn`, `python-multipart`) a `pyproject.toml` y se generó `uv.lock`.
- Se creó el registro DNS `cardiologia.futurehealthlabmx.io` (CNAME al dominio raíz, ya apuntado al VPS).
- Se verificó localmente: `docker build` exitoso, el contenedor sirve `index.html`/`assets/`, `/healthz` responde `200`, y `/api/contact` responde `500` con el mensaje de error esperado cuando faltan las credenciales SMTP (validando el camino de error de `validate.js`).
- Se actualizaron `CLAUDE.md` y `README.md` con la nueva arquitectura y los comandos para correr en local.

**Pendiente / próximos pasos:**
- Crear en GitHub los secrets `VPS_SSH_HOST`, `VPS_SSH_USER`, `VPS_SSH_PRIVATE_KEY` para que el job de despliegue funcione.
- Hacer público el paquete en GHCR tras el primer push (o loguear el VPS a `ghcr.io` con un PAT), para que `docker compose pull` no falle por falta de autenticación.
- Conseguir credenciales SMTP reales (ej. Gmail con contraseña de aplicación) y crear `/docker/cardiologia-romero-nossa/docker-compose.yml` + `.env` en el VPS (puedo hacerlo yo vía la API del VPS si me pasas las credenciales, o se hace por SSH).
- Sigue pendiente decidir el destino de `reporte.html`, `reporte 2.html`, `reporte 3.html` (quedan fuera de la imagen Docker por ahora) y de los archivos sueltos sin commitear (`Instrumental.png`, `assets/img/hero-bg.jpg`, `assets/img/testimonials/`, `assets/scss/`).
- Cuando se consiga el dominio definitivo, cambiar el `Host()` en `docker-compose.yml` y el registro DNS.

**Notas / decisiones:**
- Traefik ya corre en el VPS (`network_mode: host`, Let's Encrypt HTTP-01) como único proyecto hoy; este sitio será el segundo. El contenedor de la app no publica puertos: Traefik lo alcanza por la red del proyecto Compose usando las labels.
- Mientras se consigue el dominio final, se usa `cardiologia.futurehealthlabmx.io` (subdominio de un dominio del usuario ya apuntado al VPS).

---

## 2026-09-07 - Documentación inicial del repositorio

**Objetivo del día:**
- Dejar documentación base para que futuras sesiones (propias o con IA) entiendan rápido el proyecto.

**Hecho:**
- Se creó `CLAUDE.md` con la arquitectura del sitio (template Medilab estático, sin build, PHP de formularios no funcional, estructura de `assets/` y páginas HTML).
- Se creó este archivo `CONTROL_SESIONES.md` para llevar seguimiento del avance día a día.

**Pendiente / próximos pasos:**
- Decidir si las páginas `reporte.html`, `reporte 2.html`, `reporte 3.html` se integran al sitio o se eliminan (actualmente son borradores sin commitear).
- Revisar si los formularios de contacto/cita (`forms/contact.php`, `forms/appointment.php`) deben quedar funcionales (requieren la librería `php-email-form` que no está en el repo).
- Revisar/organizar los archivos nuevos sin commitear: `Instrumental.png`, `assets/img/hero-bg.jpg`, `assets/img/testimonials/`, `assets/scss/`.

**Notas / decisiones:**
- El proyecto es un sitio estático (HTML/CSS/JS); `main.py` y `pyproject.toml` no forman parte de la funcionalidad del sitio.
