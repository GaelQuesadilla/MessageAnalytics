def prettyDelta(seconds: int, precision=2):

    minute = 60
    hour = 60 * minute
    day = 24 * hour
    year = 365*day
    month = 30*day

    years, rem = divmod(seconds, year)
    months, rem = divmod(rem, month)
    days, rem = divmod(rem, day)
    hours, rem = divmod(rem, hour)
    minutes, secs = divmod(rem, minute)

    parts = []
    if years:
        parts.append(f"{int(years)}y")
    if months:
        parts.append(f"{int(months)}m")
    if days:
        parts.append(f"{int(days)}d")
    if hours:
        parts.append(f"{int(hours)}h")
    if minutes:
        parts.append(f"{int(minutes)}min")
    if secs or not parts:
        parts.append(f"{int(secs)}s")

    return " ".join(parts[0:precision])
