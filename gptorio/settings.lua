data:extend({
    {
        type = "string-setting",
        name = "warning",
        setting_type = "runtime-per-user",
        default_value = "Change these when the save is loaded, they won't be saved otherwise!",
        allowed_values = {"Change these when the save is loaded, they won't be saved otherwise!"},
        order = "a",
    },
    {
        type = "string-setting",
        name = "prompt",
        setting_type = "runtime-per-user",
        default_value = "a very sarcastic engineer who dislikes how everyone else builds factories and can only talk with sarcasm",
        order = "b",
        auto_trim = true,
    },
    {
        type = "string-setting",
        name = "voice",
        setting_type = "runtime-per-user",
        default_value = "en-US-AriaNeural",
        allowed_values = {"en-US-NancyNeural", "en-US-JaneNeural", "en-US-SaraNeural", "en-US-AriaNeural", "en-US-JennyNeural", "en-US-DavisNeural", "en-US-GuyNeural", "en-US-TonyNeural", "en-US-JasonNeural"},
        order = "c",
        auto_trim = true,
    },
    {
        type = "string-setting",
        name = "mood",
        setting_type = "runtime-per-user",
        default_value = "Unfriendly",
        order = "d",
        auto_trim = true,
        allowed_values = {"Default", "Angry", "Cheerful", "Excited", "Friendly", "Hopeful", "Sad", "Shouting", "Terrified", "Unfriendly", "Whispering", "Chat", "Customer-service", "Narration-professional", "Newscast-casual", "Newscast-formal", "Empathetic", "Assistant", "Newscast"}
    },
    {
        type = "int-setting",
        name = "interval",
        setting_type = "runtime-per-user",
        minimum_value = 20,
        default_value = 45,
        order = "e"
    },
    {
        type = "int-setting",
        name = "word-limit",
        setting_type = "runtime-per-user",
        minimum_value=10,
        default_value = 40,
        order = "f"
    },
    {
        type = "string-setting",
        name = "openai",
        setting_type = "runtime-per-user",
        order = "g",
        auto_trim = true,
        default_value = "OpenAIKey"
    },
    {
        type = "string-setting",
        name = "azureKey",
        setting_type = "runtime-per-user",
        order = "h",
        auto_trim = true,
        default_value = "AzureKey"
    },
    {
        type = "string-setting",
        name = "azureRegion",
        setting_type = "runtime-per-user",
        order = "i",
        auto_trim = true,
        default_value = "AzureRegion"
    },
})