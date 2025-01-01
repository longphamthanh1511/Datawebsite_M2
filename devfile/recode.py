def drain_tank_chart(request):
    # Fetch the refill time from the session, or set it to the earliest possible time
    last_drain_time = request.session.get('last_drain_time', None)
    if last_drain_time:
        last_drain_time = datetime.fromisoformat(last_drain_time)
    else:
        last_drain_time = Data.objects.earliest('time').time  # Get the earliest timestamp in the database

    # Fetch data points after the last refill time
    data = Data.objects.filter(time__gte=last_drain_time).order_by('-time')[:20]
    data = data[::-1]  # Reverse to chronological order

    # Initialize remaining water list
    drain_weights = []
    drain_tank_weight = 0

    for entry in data:
        drain_tank_weight += entry.input_weight
        drain_weights.append(min(drain_tank_weight, 0))  # Prevent negative values

    # Prepare chart data
    chart_data = {
        "labels": [entry.time.strftime('%m-%d %H:%M') for entry in data],
        "values": drain_weights,
        "threshold": DRAIN_TANK_CAPACITY  # The threshold for the alert
    }

    return render(request, 'drain_tank_chart.html', {'chart_data': chart_data})

def drain_tank(request):
    if request.method == "POST":
        # Get the user-provided refill time from the form
        refill_time = request.POST.get('drain_time')
        try:
            # Parse the user-provided time and store it in the session
            refill_time = datetime.fromisoformat(refill_time)
            request.session['last_drain_time'] = refill_time.isoformat()
        except ValueError:
            # Handle invalid date input
            return render(request, 'drain_tank.html', {'error': 'Invalid date format. Please use YYYY-MM-DD HH:MM'})

        return redirect('drain_tank_chart')  # Redirect back to the chart page

    return render(request, 'drain_tank.html')  # Render the form