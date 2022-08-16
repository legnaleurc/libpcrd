(() => {
  const shell = document.querySelectorAll('.item-title')[2].parentElement;
  const itemList = document.querySelectorAll('.item-box .itemBox > img');
  const urlList = Array.prototype.map.call(itemList, (item) => new URL(item.dataset.src, location.origin));
  const cmdList = urlList.map((url) => `curl -O ${url.toString()}`);

  const box = document.createElement('div');
  box.style.position = 'absolute';
  box.style.top = 0;
  box.style.left = 0;
  const ta = document.createElement('textarea');
  ta.rows = 80;
  ta.value = cmdList.join('\n') + '\n';
  box.appendChild(ta);
  shell.appendChild(box);
})();
