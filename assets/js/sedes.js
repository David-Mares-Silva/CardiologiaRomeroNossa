/**
 * Renders the "Sedes" (partner medical centers / locations) section from
 * assets/data/sedes.json. To add a new site, add an object to that JSON
 * file — nothing here needs to change.
 */
(function () {
  "use strict";

  const container = document.getElementById("sedes-list");
  if (!container) return;

  fetch("assets/data/sedes.json")
    .then((res) => res.json())
    .then((sedes) => {
      if (!Array.isArray(sedes) || sedes.length === 0) return;

      container.innerHTML = sedes.map(sedeCardHtml).join("");
      addStructuredData(sedes);
    })
    .catch(() => {
      // If the data can't be loaded, silently leave the section empty
      // rather than breaking the rest of the page.
    });

  function sedeCardHtml(sede) {
    const telHref = "tel:" + sede.telefono;
    const telLabel = sede.telefono_mostrar || sede.telefono;
    const mapa = sede.mapa_embed
      ? `<iframe style="border:0; width: 100%; height: 250px;" src="${sede.mapa_embed}" frameborder="0" allowfullscreen loading="lazy"></iframe>`
      : "";
    const direccion = sede.direccion
      ? `<p>${escapeHtml(sede.direccion)}</p>`
      : `<p class="fst-italic">Dirección por confirmar</p>`;

    return `
      <div class="col-lg-6 mt-4">
        <div class="info h-100">
          ${mapa}
          <div class="address mt-3">
            <i class="bi bi-hospital"></i>
            <h4>${escapeHtml(sede.institucion)}</h4>
            ${direccion}
          </div>
          <div class="phone">
            <i class="bi bi-phone"></i>
            <p><a href="${telHref}">${escapeHtml(telLabel)}</a></p>
          </div>
        </div>
      </div>`;
  }

  function addStructuredData(sedes) {
    const script = document.createElement("script");
    script.type = "application/ld+json";
    script.textContent = JSON.stringify(
      sedes
        .filter((sede) => sede.direccion)
        .map((sede) => ({
          "@context": "https://schema.org",
          "@type": "MedicalClinic",
          name: sede.institucion,
          telephone: sede.telefono,
          address: sede.direccion,
        }))
    );
    document.head.appendChild(script);
  }

  function escapeHtml(value) {
    const div = document.createElement("div");
    div.textContent = value == null ? "" : value;
    return div.innerHTML;
  }
})();
