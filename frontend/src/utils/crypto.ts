export async function encryptFile(file: File, key: Uint8Array): Promise<Blob> {
  const iv = window.crypto.getRandomValues(new Uint8Array(16));
  const algoKey = await window.crypto.subtle.importKey("raw", key, { name:"AES-GCM" }, false, ["encrypt"]);
  const content = new Uint8Array(await file.arrayBuffer());
  const ciphertext = await window.crypto.subtle.encrypt({ name:"AES-GCM", iv }, algoKey, content);
  const combined = new Uint8Array(iv.byteLength + ciphertext.byteLength);
  combined.set(iv,0);
  combined.set(new Uint8Array(ciphertext), iv.byteLength);
  return new Blob([combined], {type:file.type});
}
