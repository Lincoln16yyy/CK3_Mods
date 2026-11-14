# LOCALIZATION.md

## Why Portuguese text lives in `localization/english/`

CK3 1.20.1 ships exactly nine languages (`game/localization/languages.yml`): English,
French, German, Polish, Spanish, Simplified Chinese, Russian, Korean, Japanese. There is no
`braz_por` slot and a mod cannot create one, so a `localization/braz_por/…_l_braz_por.yml`
file would simply never be read.

The development machine runs the game in **English**, therefore the mod's strings are
written in Brazilian Portuguese inside
`Smart_Realm_Director/localization/english/srd_l_english.yml`. The game shows Portuguese
because it loads the English file, not because the engine speaks Portuguese.

Consequences to keep in mind:

- On an English install, every SRD string is Portuguese. Correct and intended.
- On a French/German/… install, SRD strings fall back to… nothing: the game looks for
  `l_french` and ours only defines `l_english`, so those players see the raw keys. Adding
  translated files later is trivial (`srd_l_french.yml`, etc.).
- Do not rename the folder or the file: `english` + `*_l_english.yml` is what makes it load.

## Format rules (enforced by `tools/validate.py`)

- UTF-8 **with BOM**, first line `l_english:`.
- One key per line: ` key:0 "text"`.
- No duplicated key anywhere in `localization/`.
- Use `\n` for line breaks inside the string.

## English originals

Kept here so the text can be reused if a language slot ever becomes available, or if the
Portuguese wording needs to be compared. (The first version of the mod shipped these.)

```
rule_srd_vassal_courtesies: "Smart Realm Director: Courtesies to Vassals"
setting_srd_vassal_courtesies_off: "Off"
setting_srd_vassal_courtesies_off_desc: "The Director does nothing. No gold is spent and no suggestions are shown."
setting_srd_vassal_courtesies_advisor: "Advisor"
setting_srd_vassal_courtesies_advisor_desc: "The Director only points out a disloyal vassal worth a courtesy. Nothing is spent and nothing changes."
setting_srd_vassal_courtesies_supervised: "Supervised"
setting_srd_vassal_courtesies_supervised_desc: "The Director prepares the courtesy and asks for your decision. Gold is only spent if you accept."
setting_srd_vassal_courtesies_auto: "Automatic"
setting_srd_vassal_courtesies_auto_desc: "The Director sends the courtesy itself, as long as the treasury stays above the reserve floor."
srd_courtesy_opinion: "Court courtesy"
srd_courtesy_opinion_desc: "The ruler took notice of us and showed it with a gift."
srd_toast_courtesy_title: "Smart Realm Director"
srd_toast_courtesy_desc: "A courtesy gift was sent to a disloyal vassal."
srd_toast_advice_title: "Smart Realm Director - advice"
srd_toast_advice_desc: "A disloyal vassal would improve with a courtesy gift."
srd_prompt_title: "A Courtesy for a Disloyal Vassal"
srd_prompt_desc: "One of your vassals holds a poor opinion of you. A gift would improve their disposition, at the cost of some gold from your treasury."
srd_prompt_accept: "Send the gift"
srd_prompt_decline: "Not now"
srd_prompt_decline_tt: "Nothing is spent and the vassal is left as they are."
srd_realm_report_decision: "Ask the Director for a Report"
srd_realm_report_decision_desc: "Ask the Smart Realm Director what it is currently allowed to do in your realm."
srd_realm_report_decision_tooltip: "Open the Director's status report."
srd_report_title: "Smart Realm Director - Status"
srd_report_option_close: "Understood"
```
