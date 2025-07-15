async function generate() {
  const prompt = document.getElementById("prompt").value;
  const mode = document.getElementById("mode").value;
  const outputDiv = document.getElementById("output");
  outputDiv.innerHTML = "⏳ Generating...";

  try {
    const response = await fetch("http://localhost:8000/dream", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ prompt: prompt, mode: mode })
    });

    const data = await response.json();
    console.log("🔥 Response from backend:", data);

    outputDiv.innerHTML = "";  // Clear loading text

    if (data.error) {
      outputDiv.innerHTML = `<div class='text-red-600 font-bold'>${data.error}</div>`;
      return;
    }

    if (!data.assets || !Array.isArray(data.assets)) {
      outputDiv.innerHTML = `<div class='text-red-600 font-bold'>Invalid response from server.</div>`;
      return;
    }

    data.assets.forEach((item) => {
      if (item.startsWith("data:image")) {
        const img = document.createElement("img");
        img.src = item;
        img.classList = "w-full rounded-lg shadow";
        outputDiv.appendChild(img);
      } else if (item.endsWith(".mp3")) {
        const audio = document.createElement("audio");
        audio.src = item;
        audio.controls = true;
        outputDiv.appendChild(audio);
      } else {
        const p = document.createElement("p");
        p.textContent = item;
        outputDiv.appendChild(p);
      }
    });

  } catch (err) {
    console.error("❌ Error:", err);
    outputDiv.innerHTML = "Something went wrong!";
  }
}
