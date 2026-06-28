# Advocacy & emergency scripts

Scout does **not** improvise in a crisis. Past-you writes fixed scripts when regulated; Scout plays them.

## Files

| File | Purpose |
|------|---------|
| `../emergency.example.yaml` | 911 / 988 / contact list, GPS fallbacks, SMS & voice scripts |
| Copy to `emergency.yaml` | Your real numbers — **never commit** |

## Flow

1. **Red button** (GPIO hold 2s) → EMS: SMS contacts with map link → call 911  
2. **Voice** `emergency` or `call 911` → same with cancel window  
3. **Crisis keywords** or `call 988` → mental health line  
4. **`contacts only`** → SMS GPS to list, no 911  

## Testing

```bash
# dry_run: true in emergency.yaml — logs only
python3 -m brain --autonomy
# say: call 988
# say: emergency
```

Test with **your own phone** as a contact before `dry_run: false`.  
**Do not** test 911 until scripts and GPS are verified.

Full guide: [docs/emergency.md](../docs/emergency.md)  
Purse build: [docs/purse-portable.md](../docs/purse-portable.md)
