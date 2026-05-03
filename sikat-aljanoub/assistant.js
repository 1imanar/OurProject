async function askAssistant() {
  const question = document.getElementById("userQuestion").value.trim();
  const reply = document.getElementById("assistantReply");

  if (question === "") {
    reply.innerHTML = "اكتب سؤالك أولًا 🌿";
    return;
  }

  reply.innerHTML = "جاري التفكير...";

  try {
    const response = await fetch("http://127.0.0.1:5000/chat", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ message: question })
    });

    const data = await response.json();
    reply.innerHTML = data.reply;

  } catch (error) {
    reply.innerHTML = "تعذر الاتصال بالمساعد.";
    console.log(error);
  }
}