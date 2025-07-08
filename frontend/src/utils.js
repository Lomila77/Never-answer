function blobToBase64(blob) {
    return new Promise((resolve, reject) => {
      const reader = new FileReader();
      reader.onloadend = () => resolve(reader.result);
      reader.onerror = reject;
      reader.readAsDataURL(blob);
    });
  }

  function textToBase64(string) {
    return new Promise((resolve, reject) => {
      const reader = new FileReader();
      reader.onloadend = () => resolve(reader.result);
      reader.onerror = reject;
      reader.readAsDataURL(blob);
    });
  }

  function base64ToBlob(base64) {
    try {
      // 處理純base64字符串（沒有data URL前綴）
      const base64Data = base64.includes(',') ? base64.split(',')[1] : base64;
      const byteCharacters = atob(base64Data);
      const byteNumbers = new Array(byteCharacters.length);
      for (let i = 0; i < byteCharacters.length; i++) {
        byteNumbers[i] = byteCharacters.charCodeAt(i);
      }
      const byteArray = new Uint8Array(byteNumbers);
      return new Blob([byteArray], { type: 'audio/wav' });
    } catch (error) {
      console.error("Base64轉Blob失敗:", error);
      return new Blob([], { type: 'audio/wav' }); // 返回空Blob而不是崩潰
    }
  }

  function base64ToText(base64) {
    const byteCharacters = atob(base64.split(',')[1]);
    let text = '';
    for (let i = 0; i < byteCharacters.length; i++) {
      text += String.fromCharCode(byteCharacters.charCodeAt(i));
    }
    return text;
  }

  export {blobToBase64, textToBase64, base64ToBlob, base64ToText};
