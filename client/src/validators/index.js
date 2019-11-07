// Проверка mime файла
export function imageType(value) {
  if (!value) return false;

  const mimes = ['image/jpeg', 'image/png', 'image/gif'];

  return mimes.includes(value);
}

// Проверка mime файла
export function docsType(value) {
  if (!value) return false;

  const mimes = [
    'application/zip',
    'application/pdf',
    'application/vnd.oasis.opendocument.text',
    'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
    'application/msword',
  ];
  return mimes.includes(value);
}

export function another(value) {
  if (!value) return true;
  return true;
}
