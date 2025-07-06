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
    const byteCharacters = atob(base64.split(',')[1]);
    const byteNumbers = new Array(byteCharacters.length);
    for (let i = 0; i < byteCharacters.length; i++) {
      byteNumbers[i] = byteCharacters.charCodeAt(i);
    }
    const byteArray = new Uint8Array(byteNumbers);
    return new Blob([byteArray], { type: 'audio/wav' });
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
