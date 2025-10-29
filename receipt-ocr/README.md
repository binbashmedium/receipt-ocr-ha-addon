# Receipt OCR Home Assistant Add-on
Ermöglicht das lesen von Kassenzettel. 

## Verwendung
1. Add-on im Store sichtbar machen:
   - Einstellungen → Add-ons → Add-on Store → Drei Punkte (⋮) → **Repositories neu laden**
2. Add-on installieren → starten
3. LibreTranslate erreichbar unter:
   http://localhost:5000/translate
4. Integration anpassen:
   url = "http://localhost:5000/ocr"
## Beispiel Card:

```
class FileUploadCard extends HTMLElement {
  setConfig(config) {
    this.config = config;
    this.innerHTML = `
      <ha-card header="${config.title || 'Kassenzettel OCR'}">
        <div id="status" style="margin:8px 0; color: var(--primary-text-color); white-space: pre-wrap;">Bereit</div>
        <input type="file" id="fileInput" accept="image/*"><br><br>
        <mwc-button id="uploadBtn" raised>Hochladen</mwc-button>
        <div id="preview" style="margin-top:10px;"></div>
        <div id="result" style="margin-top:15px; white-space: pre-wrap;"></div>
      </ha-card>
    `;

    const fileInput = this.querySelector("#fileInput");
    const uploadBtn = this.querySelector("#uploadBtn");
    const status = this.querySelector("#status");
    const preview = this.querySelector("#preview");
    const resultDiv = this.querySelector("#result");

    const OCR_URL = config.ocr_url || "http://127.0.0.1:5000/ocr";
    const STATUS_URL = config.status_url || "http://127.0.0.1:5000/status";

    // --- Helper: URL robust auflösen, ohne doppelte Basis ---
    const resolveUrl = (hass, path) => {
      try {
        // Bereits absolute URL? -> unverändert zurück
        if (/^https?:\/\//i.test(path)) return path;

        // Basis bestimmen: bevorzugt aus Home Assistant, sonst Browser-Origin
        const base =
          (hass && hass.auth && hass.auth.data && hass.auth.data.hassUrl) ||
          (hass && hass.connection && hass.connection.baseUrl) ||
          (typeof window !== "undefined" ? window.location.origin : "");

        // new URL macht die saubere Zusammensetzung (verhindert "http://http://...")
        const url = new URL(path, base).toString();
        return url;
      } catch (e) {
        console.warn("[FileUploadCard] resolveUrl() – Fallback auf Originalpfad wegen Fehler:", e);
        return path; // Fallback – sollte in der Praxis nicht nötig sein
      }
    };

    // === fetch helper mit Debug-Ausgaben ===
    const fetchMediaWithAuth = async (hass, path) => {
      console.log("[FileUploadCard] fetchMediaWithAuth() – eingehender path:", path);

      // WICHTIG: immer über resolveUrl, nicht über hass.hassUrl()
      const fullUrl = resolveUrl(hass, path);

      console.log("[FileUploadCard] fetchMediaWithAuth() – berechnete fullUrl:", fullUrl);

      // fetchWithAuth kann absolut; wir geben die fertige URL
      const res = await hass.fetchWithAuth(fullUrl);
      console.log("[FileUploadCard] fetchMediaWithAuth() – HTTP-Status:", res.status, "für", fullUrl);

      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      const blob = await res.blob();
      const objUrl = URL.createObjectURL(blob);
      console.log("[FileUploadCard] fetchMediaWithAuth() – Blob-URL erzeugt:", objUrl);
      return objUrl;
    };

    const setBusy = (b) =>
      b ? uploadBtn.setAttribute("disabled", "") : uploadBtn.removeAttribute("disabled");

    let currentObj = null;
    const setPreviewImage = (src, isObj = false) => {
      try {
        if (currentObj && typeof currentObj === "string" && currentObj.startsWith("blob:")) {
          URL.revokeObjectURL(currentObj);
        }
      } catch (e) {
        console.debug("[FileUploadCard] revokeObjectURL warn:", e);
      }
      if (isObj) currentObj = src;
      preview.innerHTML = `<img src="${src}" style="max-width:100%; border-radius:8px;">`;
    };

    // Sicherheit: alte Blob-URL beim Entfernen der Karte freigeben
    this.addEventListener("DOMNodeRemoved", () => {
      if (currentObj && currentObj.startsWith("blob:")) {
        try { URL.revokeObjectURL(currentObj); } catch (_) {}
        currentObj = null;
      }
    });

    // === Hauptlogik ===
    uploadBtn.addEventListener("click", async () => {
      const file = fileInput.files?.[0];
      if (!file) {
        status.innerText = "❗ Bitte eine Datei auswählen.";
        return;
      }

      // Lokale Vorschau anzeigen
      const reader = new FileReader();
      reader.onload = () => {
        preview.innerHTML = `<img src="${reader.result}" style="max-width:100%; border-radius:8px;">`;
      };
      reader.readAsDataURL(file);

      status.innerText = `📤 Lade "${file.name}" hoch ...`;
      resultDiv.innerText = "";
      setBusy(true);

      try {
        const formData = new FormData();
        formData.append("file", file);

        const response = await fetch(resolveUrl(this._hass, OCR_URL), { method: "POST", body: formData });
        if (!response.ok) throw new Error(`Serverfehler (${response.status})`);

        const json = await response.json();
        const filename = json.file;
        status.innerText = `⏳ OCR läuft für ${filename}...`;

        // Polling-Schleife
        const pollInterval = 4000;
        let tries = 0;
        const maxTries = 120;

        const poll = setInterval(async () => {
          tries++;
          try {
            const statusUrl = resolveUrl(this._hass, `${STATUS_URL}?file=${encodeURIComponent(filename)}`);
            const r = await fetch(statusUrl);
            if (!r.ok) return;
            const data = await r.json();

            if (data.status === "done" && data.result) {
              clearInterval(poll);
              const result = data.result;
              status.innerText = `✅ OCR abgeschlossen (${filename})`;


              // === Ergebnisse anzeigen ===
              let html = `<b>${result.store || "Unbekannter Laden"}</b><br>`;
              html += `<b>Gesamt:</b> ${result.total != null ? Number(result.total).toFixed(2) + " €" : "-"}<br><br>`;
              if (Array.isArray(result.items) && result.items.length) {
                html += `<table style="width:100%; border-collapse:collapse;">`;
                html += `<tr><th align="left">Artikel</th><th align="right">€</th></tr>`;
                result.items.forEach((it) => {
                  const qtyPart = it.qty > 1 ? it.qty + "× " : "";
                  const price = (typeof it.price === "number" ? it.price : Number(it.price || 0));
                  html += `<tr><td>${qtyPart}${it.name}</td><td align="right">${price.toFixed(2)}</td></tr>`;
                });
                html += `</table>`;
              } else {
                html += `<i>Keine Artikel erkannt</i>`;
              }
              resultDiv.innerHTML = html;
              setBusy(false);
            } else if (tries >= maxTries) {
              clearInterval(poll);
              status.innerText = "❌ Timeout beim Warten auf OCR-Ergebnis.";
              setBusy(false);
            }
          } catch (e) {
            console.warn("[FileUploadCard] Polling error:", e);
          }
        }, pollInterval);
      } catch (err) {
        status.innerText = `❌ Fehler: ${err.message}`;
        setBusy(false);
      }
    });
  }

  set hass(hass) {
    this._hass = hass;
  }
  get hass() {
    return this._hass;
  }
}

customElements.define("file-upload-card", FileUploadCard);

```
