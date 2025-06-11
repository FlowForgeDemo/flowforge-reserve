async function init() {
    await liff.init({ liffId: "あなたのLIFF_ID" });
  
    const profile = await liff.getProfile();
    const userName = profile.displayName;
    const userId = profile.userId;
  
    document.getElementById('reserve-form').addEventListener('submit', async (e) => {
      e.preventDefault();
  
      const data = {
        name: userName,
        lineId: userId,
        date: document.getElementById('date').value,
        time: document.getElementById('time').value,
        menu: document.getElementById('menu').value,
        note: document.getElementById('note').value
      };
  
      const res = await fetch('/reserve', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
      });
  
      const result = await res.json();
      document.getElementById('result').innerText = '予約が完了しました！';
    });
  }
  
  init();