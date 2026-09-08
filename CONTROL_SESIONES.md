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

## 2026-09-08 (3) - Fix de agendamiento de cita, ícono, segunda sede y testimonios

**Objetivo del día:**
- Arreglar el reporte de que "el botón de fecha no funciona" y el error al agendar cita; agregar un ícono de corazón; agregar la sede de CEMEDIC; reemplazar los textos en latín por contenido real.

**Hecho:**
- El campo de fecha de la cita tenía `type="datetime"` (tipo inválido, eliminado del estándar HTML5 hace años) y una clase `datepicker` de una librería que nunca estuvo incluida — el navegador lo mostraba como texto plano, sin calendario. Cambiado a `type="date"` (calendario nativo del navegador, sin dependencias).
- El error "No se pudo agendar la cita" es un **error real de autenticación SMTP** (confirmado en logs: `535 Username and Password not accepted` de Gmail) — no es un bug, es que `.env` todavía no tiene una contraseña de aplicación de Gmail válida.
- Agregado `logger.exception(...)` en `app/forms.py` para que la causa real de un fallo de envío quede en `docker logs` en vez de solo el mensaje genérico al usuario.
- Reemplazado el favicon y el apple-touch-icon (antes una "B" azul genérica sin relación con el sitio) por un ícono de corazón rojo, generado con Pillow (efímero, no se agregó como dependencia del proyecto).
- Agregada la sede **CEMEDIC - Centro Médico Quirúrgico de la Orinoquia** (`+57 310 481-8181`) en `assets/data/sedes.json`. No se tiene la dirección todavía — `sedes.js` ahora maneja `direccion`/`mapa_embed` como opcionales y muestra "Dirección por confirmar" en vez de romperse o inventar un dato.
- Activada la sección "Testimonios" (existía pero estaba comentada) y reemplazados los 5 textos de relleno del template ("Saul Goodman", latín de relleno) por testimonios de ejemplo en español, apropiados para una consulta de cardiología pediátrica (padres/madres de paciente, sin afirmaciones médicas específicas).
- Verificado todo reconstruyendo el contenedor local (`docker compose up --build`).

**Pendiente / próximos pasos:**
- Falta la dirección de CEMEDIC para completar esa ficha de sede.
- **Los testimonios activados son de ejemplo, no citas reales de pacientes** — reemplazar por testimonios reales (con consentimiento) cuando estén disponibles.
- Falta la contraseña de aplicación de Gmail (u otro proveedor SMTP) en `.env` para que los formularios realmente envíen correo.

**Notas / decisiones:**
- Se generó el ícono de corazón con un script de Python/Pillow ejecutado una sola vez (`uv run --with pillow`), no se agregó Pillow al proyecto.

---

## 2026-09-08 (2) - Aviso de Privacidad + botón de WhatsApp

**Objetivo del día:**
- Agregar la sección de aviso de privacidad pendiente de la sesión anterior, y un botón de WhatsApp.

**Hecho:**
- Nueva página `privacidad.html` con el Aviso de Privacidad / tratamiento de datos personales (Ley 1581 de 2012 y Decreto 1377 de 2013, Colombia): responsable, datos recolectados, finalidad, derechos del titular, cómo ejercerlos, vigencia. Usa el header/footer reales del sitio (no la plantilla genérica de `inner-page.html`). Marcada `noindex, follow` y excluida del `sitemap.xml` a propósito.
- Enlazada desde el footer ("Aviso de Privacidad", antes un `href="#"` muerto) y con una línea debajo de ambos formularios ("Al enviar este formulario aceptas nuestro Aviso de Privacidad").
- De paso, traducido el mensaje de éxito del formulario de cita, que seguía en inglés.
- Agregado botón flotante de WhatsApp (`https://wa.me/573001863974`, con mensaje prellenado) en `index.html` y `privacidad.html`, abajo a la izquierda para no chocar con el botón "volver arriba".
- Verificado en Docker: `/privacidad.html` responde 200, el botón de WhatsApp y los 3 enlaces nuevos aparecen en el HTML servido.

**Pendiente / próximos pasos:**
- **El aviso de privacidad es un borrador de buena fe, no fue revisado por un abogado** — recomendable que alguien con criterio legal lo revise antes de considerarlo definitivo.
- El número de WhatsApp (+57 300 186 3974) se usó tal como lo diste; confirmar que tiene WhatsApp Business activo y que es el número correcto para agendar citas (puede ser distinto a los teléfonos de consulta ya publicados).
- Sigue pendiente todo lo que ya estaba anotado el 2026-09-08 (sedes adicionales, testimonios placeholder, redes sociales sin perfiles reales, consentimiento de imágenes clínicas).

**Notas / decisiones:**
- Se hizo página aparte (no una sección dentro de `index.html`) porque un aviso legal largo no encaja bien en un one-pager de scroll, y es el patrón estándar (footer → página de política).

---

## 2026-09-08 - Auditoría de navegación/mejores prácticas + sección de Sedes

**Objetivo del día:**
- Verificar que no haya links rotos, revisar el sitio contra mejores prácticas para sitios de especialistas médicos, y dejar un mecanismo para agregar varios centros médicos/sedes donde se da consulta.

**Hecho:**
- Corregido un enlace de navegación roto: el menú apuntaba a `#doctores` pero la sección real tenía `id="doctors"`.
- Corregido un bug de copy real: el mensaje de éxito del formulario de contacto decía "Tu mensaje **no ha podido ser enviado**" (negativo) cuando en realidad se mostraba al enviarse correctamente.
- Corregidos `id` duplicados entre el formulario de cita y el de contacto (`id="name"`/`id="email"` se repetían en la misma página).
- `<html lang="en">` → `lang="es"` (el contenido siempre fue en español).
- Agregada meta descripción/keywords reales (estaban vacías), Open Graph, Twitter Card y datos estructurados JSON-LD (`Physician`) con los datos reales ya publicados en la página (nombre, especialidad, teléfono, dirección de Yopal).
- Agregados `robots.txt` y `sitemap.xml`, servidos por FastAPI.
- Los teléfonos del topbar y de la sección de contacto ahora son enlaces `tel:` (antes texto plano, sin click-to-call).
- Agregado `alt` descriptivo a las 18 imágenes informativas que lo tenían vacío (especialidades, doctores, galería) — investigadas visualmente para no inventar descripciones.
- Corregido typo "Adriana Romero **Nosa**" → "Nossa", y los íconos sociales de los 4 doctores (`href=""`, que recargaban la página al hacer clic) → `href="#"` en lo que se agreguen perfiles reales.
- Nueva sección **Sedes**: `assets/data/sedes.json` (mecanismo de datos, sin tocar HTML/JS para agregar una sede) + `assets/js/sedes.js` (la renderiza) + CSS. Ya tiene una sede real cargada (Medical Sky IPS, Yopal) tomada de los datos ya existentes en la página.
- Corregido un bug real de la migración anterior: `app/main.py` montaba `StaticFiles(directory="www")`, carpeta que solo existe dentro de la imagen Docker — correr la app en local sin Docker (como decía `CLAUDE.md`) fallaba. Ahora resuelve `www/` si existe (Docker) o la raíz del repo (local), sirviendo únicamente `assets/`, `index.html`, `inner-page.html`, `robots.txt` y `sitemap.xml` explícitamente (nunca el directorio completo, para no exponer `.env` ni el código de la app).
- Verificado con la app corriendo (con y sin Docker): todos los anchors internos resuelven, no quedan `id` duplicados reales, y las rutas nuevas responden 200.

**Pendiente / próximos pasos (necesitan una decisión o dato que no tengo):**
- **Sedes**: solo hay datos reales para Yopal. Para agregar Sogamoso (aparece como ciudad en el formulario de citas) u otras sedes, necesito nombre de la institución, dirección, teléfono y opcionalmente el link de Google Maps.
- **Sección "Testimonios"**: existe en el HTML pero está completamente comentada (no se ve en el sitio real) y su contenido es 100% placeholder del template original (nombres como "Saul Goodman", texto en latín de relleno). Recomendación: reemplazar por testimonios reales de pacientes (con su consentimiento) o eliminar el bloque muerto.
- **Redes sociales**: los íconos del topbar, del footer y de los 4 doctores no tienen perfiles reales enlazados. Decidir si se agregan enlaces reales o se quitan los íconos.
- **WhatsApp**: es muy usado en sitios médicos de LatAm para agendar citas; se puede agregar un botón flotante de click-to-chat si alguno de los teléfonos ya publicados tiene WhatsApp activo — falta confirmar cuál.
- **Aviso de privacidad / tratamiento de datos**: el sitio recolecta nombre, correo, teléfono y motivo de consulta por formulario sin ningún aviso de privacidad — recomendable para cumplir la Ley 1581 de 2012 (Habeas Data, Colombia). No redacté texto legal — requiere revisión de alguien con criterio legal.
- **Privacidad de imágenes clínicas**: la galería incluye una foto de un electrocardiograma con una conclusión diagnóstica real y una foto de un procedimiento quirúrgico. Confirmar que se cuenta con consentimiento para publicarlas.
- Sigue pendiente el destino de `reporte.html`, `reporte 2.html`, `reporte 3.html` y los archivos sueltos sin commitear.

**Notas / decisiones:**
- El mecanismo de sedes es deliberadamente simple (un JSON + un script, sin base de datos ni backend nuevo) para mantener la filosofía de imagen Docker ligera ya establecida.
- La imagen "medical-sky-ips.jpg" de la galería reveló que "Medical Sky IPS" es la institución real donde se da consulta en Yopal — se usó esa marca para la primera sede.

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
