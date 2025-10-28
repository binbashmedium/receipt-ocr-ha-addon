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
      <ha-card header="${config.title || 'Kassenzettel hochladen'}">
        <input type="file" id="fileInput" accept="image/*"><br><br>
        <button id="uploadBtn">Hochladen</button>
        <div id="status" style="margin-top:10px; color: var(--primary-text-color); white-space: pre-wrap;"></div>
      </ha-card>
    `;

    const status = this.querySelector("#status");
    const uploadBtn = this.querySelector("#uploadBtn");
    const fileInput = this.querySelector("#fileInput");

    uploadBtn.addEventListener("click", async () => {
      const file = fileInput.files[0];
      if (!file) {
        status.innerText = "Bitte eine Datei auswählen.";
        return;
      }

      // URL zu deinem Add-on (OCR API)
      const OCR_URL = this.config.ocr_url || "http://homeassistant.local:5000/ocr";

      status.innerText = `📤 Lade "${file.name}" hoch ...`;

      try {
        const formData = new FormData();
        formData.append("file", file);

        const response = await fetch(OCR_URL, {
          method: "POST",
          body: formData,
        });

        if (!response.ok) {
          const text = await response.text();
          throw new Error(`Fehler vom Server (${response.status}): ${text}`);
        }

        const result = await response.json();

        let output = "";
        if (result.text) {
          output = result.text.trim();
        } else if (Array.isArray(result) && result[0]?.text) {
          // falls OCR mehrere Ergebnisse zurückgibt
          output = result.map(r => r.text || "").join("\n");
        } else {
          output = JSON.stringify(result, null, 2);
        }

        status.innerText =
          `OCR erfolgreich!\n\n📄 Ergebnis:\n${output}\n\n📁 Gespeichert in /share/ocr/result.yaml`;

      } catch (err) {
        status.innerText = `Fehler beim Upload:\n${err.message || err}`;
      }
    });
  }

  // Home Assistant Kontext
  set hass(hass) {
    this._hass = hass;
  }

  get hass() {
    return this._hass;
  }
}

customElements.define("file-upload-card", FileUploadCard);
```
