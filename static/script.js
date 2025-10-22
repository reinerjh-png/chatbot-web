async function enviar() {
    const mensaje = document.getElementById("mensaje").value;
    if (!mensaje) return;

    const chat = document.getElementById("messages");
    chat.innerHTML += `<div class='msg user'>${mensaje}</div>`;

    // limpiar el campo de texto inmediatamente
    document.getElementById("mensaje").value = "";

    // enviar al backend Flask
    let res = await fetch("/chat", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({mensaje})
    });
    let data = await res.json();

    // lista de emojis suaves, solo 1 por mensaje
    const emojis = ["🤖", "😊", "👍", "💡", "🎉", "😉", "😎"];
    const emoji = emojis[Math.floor(Math.random() * emojis.length)];

    // crear burbuja vacía para el bot
    let botMsg = document.createElement("div");
    botMsg.className = "msg bot";
    chat.appendChild(botMsg);

    // efecto de tipeo letra por letra
    const respuesta = data.respuesta; // manteniendo Markdown intacto
    let i = 0;
    function escribir() {
        if (i < respuesta.length) {
            botMsg.innerHTML += respuesta.charAt(i);
            i++;
            setTimeout(escribir, 20); // velocidad del tipeo
            chat.scrollTop = chat.scrollHeight;
        } else {
            // agregar emoji al final después de escribir todo
            botMsg.innerHTML += " " + emoji;
        }
    }
    escribir();
}
