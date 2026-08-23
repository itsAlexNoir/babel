import { redirect } from '@sveltejs/kit';

// Archived is now a status facet of the unified catalogue at /books.
// This route stays as a stable, bookmarkable deep link into that view.
export function load() {
	redirect(307, '/books?status=archived');
}
