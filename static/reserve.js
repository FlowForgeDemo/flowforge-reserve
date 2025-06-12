async function init() {
  console.log("🚀 LIFF初期化開始");

  try {
    await liff.init({ liffId: "2007560400-5767wzWP" }); // 本番用LIFF IDに変更
    console.log("✅ LIFF初期化成功");

    // ← ここでログインしてないならログイン
    if (!liff.isLoggedIn()) {
      console.log("🔐 ログインしていないため、リダイレクトログインします");
      liff.login();
      return; // ← login()でリダイレクトされるので処理は一旦止める
    }

    const profile = await liff.getProfile();
    console.log("👤 プロフィール取得成功:", profile);

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

      console.log("📨 送信データ:", data);

      try {
        const res = await fetch('/reserve', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(data)
        });

        const result = await res.json();
        console.log("✅ 送信結果:", result);
        document.getElementById('result').innerText = '予約が完了しました！';
      } catch (error) {
        console.error("❌ フェッチエラー:", error);
        document.getElementById('result').innerText = '送信に失敗しました。';
      }
    });

  } catch (err) {
    console.error("❌ LIFF初期化/プロフィール取得エラー:", err);
    document.getElementById('result').innerText = 'LIFFの初期化に失敗しました。LINEアプリ内で開いてください。';
  }
}

init();