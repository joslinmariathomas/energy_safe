# Changelog

### rearrange_folders
- refactored folders and files

### extract_info_from_descriptions
- Extract three key features from the job title and description 
- `recruitment_ad` :  if it is a service ad or a job posting
- `legitimate` - if it is an ad posted by a legitimate person or company
- `license_number` - License number if available 
### add_gemini_llm_prompt
- Add llm prompt to extract necessary information from ads
### add_transformer
- add basic transformations in a new `transform` package
### Update-scraper
- Updated scraper to include extraction date
### Pagify_search_pages
- Scrape ads from 20 pages in `Locanto` ad services for electricians
### Initial commit
- Added web scraping and helper functions
