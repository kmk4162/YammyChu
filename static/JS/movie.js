setTimeout(() => {
  const box = document.getElementById('box');

  // 👇️ removes element from DOM
  box.style.display = 'none';

  // 👇️ hides element (still takes up space on page)
  // box.style.visibility = 'hidden';
}, 4300); // 👈️ time in milliseconds