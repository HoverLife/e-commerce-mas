import pandas as pd

def calculate_ctr(sessions_data):
    """
    Рассчитывает CTR по данным сеансов.
    CTR = total_clicks / total_impressions.
    sessions_data: список словарей с полями 'impressions' и 'clicks'.
    """
    if not sessions_data:
        return 0.0
    df = pd.DataFrame(sessions_data)
    total_impressions = df['impressions'].sum()
    total_clicks = df['clicks'].sum()
    if total_impressions == 0:
        return 0.0
    return total_clicks / total_impressions