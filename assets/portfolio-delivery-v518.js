// v5.18.0: local checklist interaction only; computation and packaging run in Python.
document.addEventListener('DOMContentLoaded', () => {
  const root = document.getElementById('delivery-checklist-v518');
  if (!root) return;
  const boxes = [...root.querySelectorAll('input[type="checkbox"]')];
  const status = document.createElement('p');
  status.className = 'muted';
  status.setAttribute('aria-live', 'polite');
  root.after(status);
  const update = () => {
    const done = boxes.filter(x => x.checked).length;
    status.textContent = `${done} of ${boxes.length} acceptance checks marked complete in this browser view. Export or record the formal checklist separately.`;
  };
  boxes.forEach(x => x.addEventListener('change', update));
  update();
});
