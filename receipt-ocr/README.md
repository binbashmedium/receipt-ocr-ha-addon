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
        <button id="uploadBtn">Hochladen</button>
        <div id="preview" style="margin-top:10px;"></div>
        <div id="result" style="margin-top:15px; white-space: pre-wrap;"></div>
      </ha-card>
    `;

    const fileInput = this.querySelector("#fileInput");
    const uploadBtn = this.querySelector("#uploadBtn");
    const status = this.querySelector("#status");
    const preview = this.querySelector("#preview");
    const resultDiv = this.querySelector("#result");

    // Standard URLs
    const OCR_URL = config.ocr_url || "http://127.0.0.1:5000/ocr";
    const STATUS_URL = config.status_url || "http://127.0.0.1:5000/status";

    uploadBtn.addEventListener("click", async () => {
      const file = fileInput.files[0];
      if (!file) {
        status.innerText = "❗ Bitte eine Datei auswählen.";
        return;
      }

      // Vorschau direkt anzeigen
      const reader = new FileReader();
      reader.onload = () => {
        preview.innerHTML = `<img src="${reader.result}" style="max-width:100%; border-radius:8px;">`;
      };
      reader.readAsDataURL(file);

      status.innerText = `📤 Lade "${file.name}" hoch ...`;
      resultDiv.innerText = "";

      try {
        const formData = new FormData();
        formData.append("file", file);

        // Upload starten
        const response = await fetch(OCR_URL, {
          method: "POST

```
