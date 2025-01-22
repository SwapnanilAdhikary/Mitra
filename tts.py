from resemble import Resemble

# Set the Resemble API key
Resemble.api_key('fOZfKirwfnXTgQekOMhBrQtt')


def create_audio_clip(project_uuid, voice_uuid, text_body):
    try:
        # Create a synchronous clip
        response = Resemble.v2.clips.create_sync(
            project_uuid,
            voice_uuid,
            text_body,
            title=None,
            sample_rate=None,
            output_format=None,
            precision=None,
            include_timestamps=None,
            is_archived=None,
            raw=None
        )

        # Extract and return the audio URL
        audio_url = response['item']['audio_src']
        return audio_url
    except Exception as e:
        return f"An error occurred: {e}"

# Example usage
# Get the default Resemble project and voice UUIDs
project_uuid = Resemble.v2.projects.all(1, 10)['items'][0]['uuid']
voice_uuid = Resemble.v2.voices.all(1, 10)['items'][0]['uuid']

# Text to convert to speech
text_body = 'hello comrades'

# Call the function to create the audio clip
audio_url = create_audio_clip(project_uuid, voice_uuid, text_body)

# Print the audio URL
print("Generated Audio URL:", audio_url)
