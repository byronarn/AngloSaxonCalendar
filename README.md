This script, [ascal-md.py]() creates a Markdown file with the dates for my reconstructed calendar for the specified year.

`ascal-md.py` is all you need. The only dependency that it requires is pyephem. Install this in your Python environment with `pip install pyephem`.

The way it determines the beginning of the month is that it calculates the moon illumination at sunset for each day starting at the new moon. The day where the moon illumination is greater than 1% will begin the month. Comparing my results with actual moon sighting websites finds that this yields very high accuracy.

I have included a sample output file, [ascal-md.py](https://github.com/byronpendason/ascal-md.py/blob/1a8cc7e6f7e27cc3a1cfc5cd41822f3cf017e76b/ascal-2022.md).

For information on this calendar, see [my blog](https://www.minewyrtruman.com/anglosaxoncalendar).
