function blobToBase64(blob) {
    return new Promise((resolve, reject) => {
        const reader = new FileReader();
        reader.onloadend = () => {
            // onloadend donne un DataURL, il faut enlever le préfixe
            const base64data = reader.result.split(',')[1];
            resolve(base64data);
        };
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

  function base64ToBlob(base64, mime = 'audio/wav') {
    const base64Data = base64.includes(',') ? base64.split(',')[1] : base64;

    const byteCharacters = atob(base64Data);
    const byteNumbers = new Array(byteCharacters.length);
    for (let i = 0; i < byteCharacters.length; i++) {
      byteNumbers[i] = byteCharacters.charCodeAt(i);
    }
    const byteArray = new Uint8Array(byteNumbers);
    return new Blob([byteArray], { type: mime });
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
