let lastGeminiRequestTime = 0;
const GEMINI_MIN_INTERVAL = 10000; // 10 seconds

// Tab switching logic
const tabBtns = document.querySelectorAll('.tab-btn');
const tabContents = document.querySelectorAll('.tab-content');
tabBtns.forEach(btn => {
  btn.addEventListener('click', () => {
    tabBtns.forEach(b => b.classList.remove('active'));
    btn.classList.add('active');
    const tab = btn.getAttribute('data-tab');
    tabContents.forEach(tc => tc.classList.add('hidden'));
    document.getElementById('tab-' + tab).classList.remove('hidden');
    if(tab === 'game') document.getElementById('game-copy-msg').classList.add('hidden');
  });
});

async function generate(mode, event) {
  const now = Date.now();
  if (now - lastGeminiRequestTime < GEMINI_MIN_INTERVAL) {
    document.getElementById('output-' + mode).innerHTML = `<div class='text-yellow-400 font-bold'>Please wait a few seconds before generating again to avoid using up your AI quota.</div>`;
    return;
  }
  lastGeminiRequestTime = now;

  const button = event?.target;
  button.disabled = true;
  button.innerHTML = "Generating <span class='spinner'></span>";
  const prompt = document.getElementById('prompt-' + mode).value;
  const outputDiv = document.getElementById('output-' + mode);
  outputDiv.innerHTML = "⏳ Generating...";

  let language = undefined;
  if(mode === 'game') {
    language = document.getElementById('language-select').value;
  }

  let word_count = undefined;
  if (mode === 'story') {
    // Optionally, you can add a word count input and read it here
  }

  try {
    const body = { prompt: prompt, mode: mode };
    if (mode === 'game') body.language = language;
    if (mode === 'story') body.word_count = word_count;
    const response = await fetch("http://localhost:8000/dream", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify(body)
    });

    const data = await response.json();
    outputDiv.innerHTML = "";

    if (data.error) {
      outputDiv.innerHTML = `<div class='text-red-600 font-bold'>${data.error}</div>`;
      return;
    }
    if (!data.assets || !Array.isArray(data.assets)) {
      outputDiv.innerHTML = `<div class='text-red-600 font-bold'>Invalid response from server.`;
      return;
    }
    const item = data.assets[0];
    if (mode === "image" && item.startsWith("data:image")) {
      const img = document.createElement("img");
      img.src = item;
      img.classList = "w-full rounded-lg shadow";
      outputDiv.appendChild(img);
    } else if (mode === "game") {
      // Show code in a code block with copy button
      const pre = document.createElement("pre");
      const code = document.createElement("code");
      code.textContent = item;
      pre.appendChild(code);
      outputDiv.appendChild(pre);
      // Copy button
      const copyBtn = document.createElement("button");
      copyBtn.textContent = "Copy Code";
      copyBtn.className = "deepai-btn mt-2";
      copyBtn.onclick = () => {
        navigator.clipboard.writeText(item);
        copyBtn.textContent = "Copied!";
        setTimeout(() => copyBtn.textContent = "Copy Code", 1500);
      };
      outputDiv.appendChild(copyBtn);
      document.getElementById('game-copy-msg').classList.remove('hidden');
    } else if (mode === "story") {
      const p = document.createElement("p");
      p.textContent = item;
      outputDiv.appendChild(p);
    } else {
      const p = document.createElement("p");
      p.textContent = item;
      outputDiv.appendChild(p);
    }
  } catch (err) {
    outputDiv.innerHTML = "Something went wrong!";
  } finally {
    button.disabled = false;
    button.innerHTML = mode === 'story' ? "Generate Story" : mode === 'image' ? "Generate Image" : "Generate Game Code";
  }
}
