const { Client, LocalAuth } = require('whatsapp-web.js');
const qrcode = require('qrcode-terminal');
const GEMINI_API_KEY = process.env.GEMINI_API_KEY;
const client = new Client({ authStrategy: new LocalAuth(), puppeteer: { args: ['--no-sandbox', '--disable-setuid-sandbox'] } });

client.on('qr', (qr) => { qrcode.generate(qr, {small: true}); });
client.on('ready', () => { console.log('Bot Ready Hai!'); });

client.on('message', async msg => {
    if (msg.from.includes('@g.us')) return;
    if (msg.body.toLowerCase() === 'hi' || msg.body.toLowerCase() === 'hello') {
        msg.reply('Assalam o Alaikum! Main Yasir Bot hun. Kuch bhi pucho, translate karwana ho ya parhai ka sawal ho, sab bata dunga.');
        return;
    }
    try {
        const response = await fetch(`https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key=${GEMINI_API_KEY}`, {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({ contents: [{ parts: [{ text: `Tum ek smart AI assistant ho jaise ChatGPT. User jo bhi puche uska pura aur sahi jawab do. Chahe wo parhai ho, janwar, science, history, coding, ya translate ho. Agar user kahe Urdu me translate karo to Urdu me karo, English me to English me, Spanish me to Spanish me. User jis language me puche usi language me jawab do. User ka sawal: ${msg.body}` }] }] })
        });
        const data = await response.json();
        msg.reply(data.candidates[0].content.parts[0].text);
    } catch (e) { msg.reply('Thora wait karo, dobara pucho.'); }
});
client.initialize();
