#include <wchar.h>

__declspec(dllexport) const wchar_t* get_localized_string(const wchar_t* key, const wchar_t* lang) {
    if (wcscmp(key, L"menu.play_btn") == 0) {
        if (wcscmp(lang, L"russian") == 0) return L"Играть!";
        return L"Play!";
    }
    if (wcscmp(key, L"menu.settings_btn") == 0) {
        if (wcscmp(lang, L"russian") == 0) return L"Настройки";
        return L"Settings";
    }
    if (wcscmp(key, L"settings.name") == 0) {
        if (wcscmp(lang, L"russian") == 0) return L"Настройки";
        return L"Settings";
    }
    if (wcscmp(key, L"settings.lang_text") == 0) {
        if (wcscmp(lang, L"russian") == 0) return L"Язык:";
        return L"Lang:";
    }
    if (wcscmp(key, L"settings.lang") == 0) {
        if (wcscmp(lang, L"russian") == 0) return L"Русский";
        return L"English";
    }
    return L"Unknown";
}