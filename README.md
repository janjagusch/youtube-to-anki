# youtube-to-anki

Converts a YouTube video into Anki Cards.

Takes a YouTube video with audio in your target language and transcript (subtitles) in your native language and converts it into an `.apkg` file that can easily be imported into Anki. The Anki cards have the target language audio on the front and the native language transcript on the back. I hope this helps improving your listening comprehension.

## Installation

### `conda`

The preferred way to install this package is using [conda](https://github.com/conda/conda):

```
conda install youtube-to-anki
```

### `pip`

You can also install it through pip:

```
pip install youtube-to-anki
```

However, when you install this package though `pip`, you will have to manually install [ffmpeg](https://ffmpeg.org/download.html) afterwards.

## Usage

### CLI

You can use the command like interface like this:

```
youtube-to-anki <video_id>
```

Where `<video_id>` can be extracted from a YouTube URL like this:

`https://www.youtube.com/watch?v=<video_id>`

There are some CLI options you can provide, for example for choosing the transcript language. Check `youtube-to-anki --help` for details.

## Importing to Anki

youtube-to-anki produces an `.apkg` file, which can easily be imported into Anki. In Anki, just click "File" -> "Import".

## Listing Available Transcripts

youtube-to-anki calls [youtube-transcript-api](https://github.com/jdepoix/youtube-transcript-api) for requesting the video transcripts. If you're unsure what value to provide to the `--transcript-language` option, you can list all available languages with `youtube_transcript_api --list-transcripts <video_id>`.
