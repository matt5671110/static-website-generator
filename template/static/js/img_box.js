const options = {
	// Background Color (Default: 'rgba(0,0,0,0.9)')
	bgColor: 'rgba(0,0,0,0.9)',
	// Fade-in and fade-out duration (Default: 300)
	fadeDurationMs: 300,
	// Hide scrollbar when showing img_box (Default: true)
	hideScroll: true,
	// img_box z inedx (Default: 1000)
	zIndex: 2000,

	// Color of frame used when caption is present (Default: 'white')
	frameColor: 'white',
	// Color of caption text (Default: 'black')
	captionColor: 'black',
	// Font size of caption (Default: '1.5rem')
	captionFontSize: '1.5rem',
	// Font family of caption (Default: 'inital')
	captionFontFamily: '"Liberation Serif", "Times New Roman", serif'
};

function img_box(self) {
	const container = initContainer();
	const img_url = (typeof self.getAttribute('data-hires') === "string") ? self.getAttribute('data-hires') : self.src;
	const body_overflow = document.body.style.overflow;
	const caption = (typeof self.getAttribute("data-caption") === "string") ? self.getAttribute("data-caption") : null;

	const figure = (caption) ? document.createElement('figure') : null;
	if(figure) {
		figure.style.display = 'flex';
		figure.style.flexDirection = 'column';
		figure.style.alignItems = 'center';
		figure.style.justifyContent = 'center';
		figure.style.backgroundColor = options.frameColor;
		figure.style.padding = '0.5rem';
		figure.style.margin = 'auto';
		figure.style.maxWidth = '90%';
		figure.style.maxHeight = '90%';

	}

	const img = new Image();
	img.src = img_url;
	if(figure) {
		img.style.maxWidth = '100%';
		img.style.maxHeight = 'calc(75vh - 3rem)';
		figure.appendChild(img);
		if(caption) {
			const figcaption = document.createElement('figcaption');
			figcaption.innerText = caption;
			figcaption.style.color = options.captionColor;
			figcaption.style.fontSize = options.captionFontSize;
			figcaption.style.fontFamily = options.captionFontFamily;
			figcaption.style.padding = '1rem';
			figcaption.style.marginBottom = '-0.5rem';
			figure.appendChild(figcaption);
		}
		container.appendChild(figure);
	}
	else {
		img.style.maxWidth = '90%';
		img.style.maxHeight = '90%';
		img.style.margin = 'auto';
		container.appendChild(img);
	}
	container.style.display = 'flex';

	if(options.hideScroll) {
		document.body.style.overflow = 'hidden'
	}

	window.setTimeout(() => container.style.opacity = 1,0);

	const onClick = function() {
		container.removeEventListener('click', onClick);
		container.style.opacity = 0;
		window.setTimeout(function() {
			container.style.display = 'none';
			container.innerHTML = '';
			document.body.style.overflow = body_overflow;
		}, options.fadeDurationMs * 0.8);
	}

	container.addEventListener('click', onClick);
}

let img_box_container;
const initContainer = function() {
	if (img_box_container) return img_box_container;

	img_box_container = document.createElement('div');
	img_box_container.id = 'img_box';
	img_box_container.style.top = '0px';
	img_box_container.style.left = '0px';
	img_box_container.style.opacity = 0;
	img_box_container.style.width = '100%';
	img_box_container.style.height = '100%';
	img_box_container.style.display = 'none';
	img_box_container.style.position = 'fixed';
	img_box_container.style.cursor = 'pointer';
	img_box_container.style.zIndex = options.zIndex;
	img_box_container.style.backgroundColor = options.bgColor;
	img_box_container.style.transition = 'opacity ' + options.fadeDurationMs + 'ms';

	document.body.appendChild(img_box_container);

	return img_box_container;
}
