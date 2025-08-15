from ydata_profiling import ProfileReport

def build_profile_html(pdf):
    profile = ProfileReport(
        pdf,
        title="Data Profiling Report",
        explorative=True
    )
    return profile.to_html()
