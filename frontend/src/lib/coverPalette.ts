// Generated-cover palette for books with no cover image.
// Ground/ink pairs are specified in oklch and gamut-fitted to sRGB (see docs/design-system.md);
// every pair holds at least 7.2:1 contrast so titles stay readable at thumbnail size.
const PALETTE: [ground: string, ink: string][] = [
	['#f6e3e0', '#6e3330'],
	['#f2e6d9', '#643e03'],
	['#e7ead9', '#474d0a'],
	['#ddede2', '#175533'],
	['#d8edee', '#005256'],
	['#dde9f6', '#1f4a73'],
	['#e7e6f6', '#483f72'],
	['#f1e3ef', '#61355d'],
];

/** Deterministic hash of a string into a small non-negative integer. */
function hashString(s: string): number {
	let h = 0;
	for (let i = 0; i < s.length; i++) {
		h = (h * 31 + s.charCodeAt(i)) | 0;
	}
	return Math.abs(h);
}

/** Picks a stable (ground, ink) pair for a book's generated cover from its title. */
export function coverTint(title: string): { ground: string; ink: string } {
	const [ground, ink] = PALETTE[hashString(title) % PALETTE.length];
	return { ground, ink };
}
