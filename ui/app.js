(() => {
  const gallery = document.getElementById("gallery");
  const statusBar = document.getElementById("status-bar");
  const emptyState = document.getElementById("empty-state");
  const countBar = document.getElementById("count-bar");
  const btnExtract = document.getElementById("btn-extract");
  const searchInput = document.getElementById("search");
  const filterType = document.getElementById("filter-type");
  const lightbox = document.getElementById("lightbox");
  const lbImg = document.getElementById("lb-img");
  const lbName = document.getElementById("lb-name");
  const lbInfo = document.getElementById("lb-info");
  const lbDownload = document.getElementById("lb-download");

  let allImages = [];
  let currentIndex = -1;
  let filteredImages = [];

  function fmtSize(bytes) {
    if (bytes < 1024) return bytes + " B";
    if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(1) + " KB";
    return (bytes / (1024 * 1024)).toFixed(1) + " MB";
  }

  function showStatus(msg, type = "") {
    statusBar.textContent = msg;
    statusBar.className = "status-bar" + (type ? " " + type : "");
  }

  function makeCard(img, idx) {
    const card = document.createElement("div");
    card.className = "card";

    const thumb = document.createElement("img");
    thumb.className = "card-thumb";
    thumb.src = "/images/" + encodeURIComponent(img.name);
    thumb.alt = img.name;
    thumb.loading = "lazy";

    const footer = document.createElement("div");
    footer.className = "card-footer";

    const extBadge = document.createElement("span");
    extBadge.className = "card-ext";
    extBadge.textContent = img.ext;

    const sizeBadge = document.createElement("span");
    sizeBadge.className = "card-size";
    sizeBadge.textContent = fmtSize(img.size);

    footer.appendChild(extBadge);
    footer.appendChild(sizeBadge);
    card.appendChild(thumb);
    card.appendChild(footer);

    card.addEventListener("click", () => openLightbox(idx));
    return card;
  }

  function renderGallery() {
    const query = searchInput.value.trim().toLowerCase();
    const typeFilter = filterType.value;

    filteredImages = allImages.filter(img => {
      if (typeFilter && img.ext !== typeFilter) return false;
      if (query && !img.name.toLowerCase().includes(query)) return false;
      return true;
    });

    while (gallery.firstChild) gallery.removeChild(gallery.firstChild);

    if (filteredImages.length === 0) {
      emptyState.classList.remove("hidden");
      countBar.textContent = "";
      return;
    }

    emptyState.classList.add("hidden");

    const fragment = document.createDocumentFragment();
    filteredImages.forEach((img, idx) => fragment.appendChild(makeCard(img, idx)));
    gallery.appendChild(fragment);

    countBar.textContent =
      filteredImages.length + " image" + (filteredImages.length !== 1 ? "s" : "");
  }

  async function loadImages() {
    try {
      const res = await fetch("/api/images");
      allImages = await res.json();
      renderGallery();
      if (allImages.length === 0) emptyState.classList.remove("hidden");
    } catch (_) {
      showStatus("Could not connect to server.", "error");
    }
  }

  async function extractCache() {
    btnExtract.disabled = true;
    document.getElementById("extract-label").textContent = "Extracting…";
    showStatus("Scanning Discord cache, please wait…");

    try {
      const res = await fetch("/api/extract");
      const data = await res.json();
      if (data.error) {
        showStatus("Error: " + data.error, "error");
      } else {
        const n = data.extracted;
        showStatus("Done — " + n + " image" + (n !== 1 ? "s" : "") + " extracted.", "success");
        await loadImages();
      }
    } catch (_) {
      showStatus("Extraction failed. Is the server running?", "error");
    } finally {
      btnExtract.disabled = false;
      document.getElementById("extract-label").textContent = "Extract Cache";
    }
  }

  function openLightbox(idx) {
    currentIndex = idx;
    const img = filteredImages[idx];
    lbImg.src = "/images/" + encodeURIComponent(img.name);
    lbImg.alt = img.name;
    lbName.textContent = img.name;
    lbInfo.textContent = img.ext + " · " + fmtSize(img.size);
    lbDownload.href = "/images/" + encodeURIComponent(img.name);
    lbDownload.download = img.name;
    lightbox.classList.remove("hidden");
    document.body.style.overflow = "hidden";
  }

  function closeLightbox() {
    lightbox.classList.add("hidden");
    document.body.style.overflow = "";
    lbImg.src = "";
  }

  function navigate(dir) {
    const next = currentIndex + dir;
    if (next >= 0 && next < filteredImages.length) openLightbox(next);
  }

  btnExtract.addEventListener("click", extractCache);
  searchInput.addEventListener("input", renderGallery);
  filterType.addEventListener("change", renderGallery);

  document.getElementById("lb-close").addEventListener("click", closeLightbox);
  document.getElementById("lb-prev").addEventListener("click", () => navigate(-1));
  document.getElementById("lb-next").addEventListener("click", () => navigate(1));

  lightbox.addEventListener("click", e => { if (e.target === lightbox) closeLightbox(); });

  document.addEventListener("keydown", e => {
    if (lightbox.classList.contains("hidden")) return;
    if (e.key === "Escape") closeLightbox();
    if (e.key === "ArrowLeft") navigate(-1);
    if (e.key === "ArrowRight") navigate(1);
  });

  loadImages();
})();
