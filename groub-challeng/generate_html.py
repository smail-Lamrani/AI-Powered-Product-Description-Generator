import json
from pathlib import Path

def build_html():
    desc_dir = Path("data/descriptions")
    categories = [p.stem for p in desc_dir.glob("*.json")]

    products_by_category = {}
    for cat in categories:
        with open(desc_dir / f"{cat}.json", "r", encoding="utf-8") as f:
            products_by_category[cat] = json.load(f)

    with open("product_describer.html", "w", encoding="utf-8") as f:
        f.write("""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Product Descriptions</title>
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
  <style>
    .description { font-style: italic; color: #555; }
    .product-card { margin-bottom: 20px; }
    .product-image { height: 150px; object-fit: contain; }
  </style>
</head>
<body class="p-4">
  <h1 class="text-center mb-4">🛍️ AI Product Descriptions</h1>

  <div class="container mb-4">
    <div class="row justify-content-center g-2">
      <div class="col-md-4">
        <select id="categoryFilter" class="form-select">
          <option value="">All Categories</option>
""")

        # Add categories
        for cat in categories:
            f.write(f'<option value="{cat}">{cat}</option>\n')

        f.write("""        </select>
      </div>
      <div class="col-md-4">
        <input type="text" id="searchInput" placeholder="Search by name..." class="form-control">
      </div>
    </div>
  </div>

  <div class="container">
    <div class="row" id="productContainer">
    </div>
  </div>

  <script>
    const descriptions = {};
""")

        # Inject product data
        for cat in categories:
            f.write(f'descriptions["{cat}"] = {json.dumps(products_by_category[cat])};\n')

        # JavaScript logic
        f.write("""
    function updateUI() {
      const container = document.getElementById("productContainer");
      container.innerHTML = "";
      const category = document.getElementById("categoryFilter").value;
      const query = document.getElementById("searchInput").value.toLowerCase();

      const filtered = Object.entries(descriptions)
        .filter(([cat]) => !category || cat === category)
        .flatMap(([, items]) => items)
        .filter(p => p.title.toLowerCase().includes(query));

      for (let p of filtered) {
        container.innerHTML += `
          <div class="col-md-4">
            <div class="card product-card h-100">
              <img src="${p.thumbnail}" class="card-img-top product-image" alt="${p.title}">
              <div class="card-body">
                <h5 class="card-title">${p.title}</h5>
                <p><strong>Brand:</strong> ${p.brand} <br> 💵 ${p.price}$ | ⭐ ${p.rating} | 📦 ${p.availabilityStatus}</p>
                <p class="description">${p.generated_description}</p>
              </div>
            </div>
          </div>`;
      }
    }

    document.getElementById("categoryFilter").addEventListener("change", updateUI);
    document.getElementById("searchInput").addEventListener("input", updateUI);
    updateUI();
  </script>
</body>
</html>""")

    print("HTML file generated: product_describer.html")

if __name__ == "__main__":
    build_html()
