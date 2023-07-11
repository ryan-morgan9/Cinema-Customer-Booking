from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.utils.timezone import datetime
from .models import Showings,Screen,Booking,PaymentDetails

import datetime

#Ryan Morgan

#Define prices of tickets.
ticketPrices = { "adult": 10,
"student": 7.5,
"child": 5}

# Create your views here.
def home(request):
    return render(request, "cust/base.html")

def selectDate(request):
    #get list of dates of showings and sort them.
    getDates = Showings.objects.values('showingDate').distinct().order_by('showingDate')
    #Format dates for display and parameter passing.
    showingDates = []
    for dates in getDates:
        showingDates.append(dates['showingDate'].strftime('%d-%m-%Y'))

    if request.method == "POST":
        #get selected date
        selectedDate = request.POST['showingDate']
        #pass date to booking view
        return redirect('booking',selectedDate=selectedDate)
        
    #load list of dates into HTML page.
    return render(request, "cust/showingDates.html",
        {
            'showingDates': showingDates,
        })

def booking(request, selectedDate):
    if request.method == "GET":
        #receive date passed in and reformat for DB functions
        receivedDate = datetime.datetime.strptime(selectedDate, "%d-%m-%Y").date()
        #get showings on selected date.
        getShowings = Showings.objects.filter(showingDate = receivedDate)
        #pass date, showings, and ticket prices into HTML page for display
        return render(request, "cust/booking.html",
        {
            'selectedDate': selectedDate,
            'getShowings': getShowings,
            'ticketPriceAdult': ticketPrices['adult'],
            'ticketPriceStudent': ticketPrices['student'],
            'ticketPriceChild': ticketPrices['child'],
        })
    if request.method == "POST":
        #Get booking details from HTML form
        adultQuantity = request.POST['adultQuantity']
        studentQuantity = request.POST['studentQuantity']
        childQuantity = request.POST['childQuantity']
        selectedShowing = request.POST['selectedShowing']

        #get booking from DB based on what the user has selected.
        show = Showings.objects.get(id = selectedShowing)

        print(selectedShowing)

        #get cinema screen for selected showing.
        screenCap = Screen.objects.get(id=show.screen_id)
        #calculate total number of tickets.
        totalTickets = (int(adultQuantity) + int(studentQuantity) + int(childQuantity))

        #if the user hasn't selected any tickets, send them back
        if (totalTickets == 0):
            print("No tickets were selected.")
            return redirect('booking',selectedDate=selectedDate)

        #if the number of tickets the user has selected overflows the screen capacity, then reject booking
        if ((show.ticketsSold + totalTickets) > screenCap.capacity):
            print("Screen insufficient seats available.")
            return redirect('selectDate')

        #send them to payment screen
        return redirect('payment',adultQuantity=adultQuantity, studentQuantity=studentQuantity, childQuantity=childQuantity, selectedShowing=selectedShowing)
        
    return redirect('booking',selectedDate=selectedDate)

def payment(request,adultQuantity, studentQuantity, childQuantity, selectedShowing):
    if request.method == "GET":
        #get selected showing
        try:
            show = Showings.objects.get(id=selectedShowing)
        except Showings.DoesNotExist:
            print("didn't find show")
            return redirect('home')

        #if showing is not found then send them back (validation)
        if show is None:
            print("didn't find show")
            return redirect('home')
        #load payment page and load in showing for display.
        return render(request, "cust/payment.html",
        {
            'show': show,
        })
    if request.method == "POST":
        #get payment details from HTML form.
        cardholderName = request.POST['cardholderName']
        cardNumber = request.POST['cardNumber']
        expiryDate = request.POST['expiryDate']
        cardType = request.POST['cardType']

        #find whether payment details have been used before, otherwise save them
        try:
            existingPayment = PaymentDetails.objects.get(cardholderName=cardholderName, cardNumber=cardNumber, expiryDate=expiryDate, cardType=cardType)
        except PaymentDetails.DoesNotExist:
            newPayment = PaymentDetails(cardholderName=cardholderName,cardNumber=cardNumber,expiryDate=expiryDate,cardType=cardType)
            newPayment.save()
            existingPayment = newPayment
        # if existingPayment is None:
        #     newPayment = PaymentDetails(cardholderName=cardholderName,cardNumber=cardNumber,expiryDate=expiryDate,cardType=cardType)
        #     newPayment.save()
        #     existingPayment = newPayment

        #get selected showing
        try:
            getShowing = Showings.objects.get(id=selectedShowing)
        except PaymentDetails.DoesNotExist:
            return redirect("home")
            
        #calculate total cost of booking
        totalCost = ((adultQuantity * ticketPrices["adult"]) + (studentQuantity * ticketPrices["student"]) + (childQuantity * ticketPrices["child"]))

        #calculate total number of tickets sold for booking and save them to DB
        getShowing.ticketsSold += (adultQuantity + studentQuantity + childQuantity)
        getShowing.save()

        #Save new booking to DB
        newBooking = Booking(showingRef = getShowing, ticketQuantity = (adultQuantity + studentQuantity + childQuantity), totalCost = totalCost, paymentRef=existingPayment)
        newBooking.save()

        #Back to home page
        return redirect("home")

def getPayment_Modify(request):
    if request.method == "POST":
        #get payment details used for booking
        cardholderName = request.POST['cardholderName']
        cardNumber = request.POST['cardNumber']
        expiryDate = request.POST['expiryDate']
        cardType = request.POST['cardType']

        #try to retrieve payment details in DB
        try:
            existingPayment = PaymentDetails.objects.get(cardholderName=cardholderName, cardNumber=cardNumber, expiryDate=expiryDate, cardType=cardType)
        except PaymentDetails.DoesNotExist:
            return redirect("getPayment_Modify")

        #Send to booking modification page with paymentID
        return redirect("modifyBooking", payment_id = existingPayment.id)

    return render(request, "cust/enterPayment.html")

def modifyBooking(request, payment_id):
    #Get booking related to payment details
    try:
        booking_list = Booking.objects.filter(paymentRef=payment_id).values('id', 'showingRef', 'ticketQuantity', 'totalCost', 'paymentRef')
    except Booking.DoesNotExist:
        return redirect("getPayment_Modify")

    if request.method == "POST":
        #Get booking that is to be changed and send to page to change the showing.
        selectedBooking = request.POST['selectedBooking']
        return redirect("changeShowing", selectedBooking=selectedBooking)
    return render(request, "cust/modifyBooking.html",
        {
            'booking_list': booking_list,
        })

def changeShowing(request, selectedBooking):
    #get all showings to choose from
    showing_list = Showings.objects.all()
    if request.method == "POST":
        #Get the new showing selected and change booking so that it is for that newly selected showing and save to DB.
        new_showing = request.POST['new_showing']
        get_showing = Showings.objects.get(id=new_showing)
        current_booking = Booking.objects.get(id=selectedBooking)
        #replace old showing for new showing
        current_booking.showingRef = get_showing
        current_booking.save()
        return redirect("getPayment_Modify")
    return render(request, "cust/chooseNewShowing.html",
        {
            'showing_list': showing_list,
        })

def getPayment_Delete(request):
    if request.method == "POST":
        #get payment details used for booking
        cardholderName = request.POST['cardholderName']
        cardNumber = request.POST['cardNumber']
        expiryDate = request.POST['expiryDate']
        cardType = request.POST['cardType']

        #try to retrieve payment details in DB
        try:
            existingPayment = PaymentDetails.objects.get(cardholderName=cardholderName, cardNumber=cardNumber, expiryDate=expiryDate, cardType=cardType)
        except PaymentDetails.DoesNotExist:
            return redirect("getPayment_Modify")

        #go to deletion page with paymentID
        return redirect("deleteBooking", payment_id = existingPayment.id)

    return render(request, "cust/enterPayment.html")

def deleteBooking(request,payment_id):
    #get booking in relation to payment details
    try:
        booking_list = Booking.objects.filter(paymentRef=payment_id).values('id', 'showingRef', 'ticketQuantity', 'totalCost', 'paymentRef')
    except Booking.DoesNotExist:
        return redirect("getPayment_Delete")

    if request.method == "POST":
        #get booking that is to be deleted
        selectedBooking = request.POST['selectedBooking']
        get_booking_delete = Booking.objects.get(id=selectedBooking)
        get_booking = Booking.objects.filter(id=selectedBooking).values('id', 'showingRef', 'ticketQuantity')
        #get showing that is part of booking
        try:
            get_showing = Showings.objects.get(id=get_booking[0]['showingRef'])
        except Showings.DoesNotExist:
            return redirect("getPayment_Delete")

        #adjust the number of seats available for the cancellation
        if (get_showing.ticketsSold - get_booking[0]['ticketQuantity']) >= 0:
            get_showing.ticketsSold -= get_booking[0]['ticketQuantity']
            get_showing.save()
        else:
            return redirect("getPayment_Delete")

        #delete booking
        get_booking_delete.delete()

        return redirect("getPayment_Delete")
    return render(request, "cust/deleteBooking.html",
        {
            'booking_list': booking_list,
        })

def getPayment_View(request):
    if request.method == "POST":
        #get payment details used for booking
        cardholderName = request.POST['cardholderName']
        cardNumber = request.POST['cardNumber']
        expiryDate = request.POST['expiryDate']
        cardType = request.POST['cardType']

        #try to retrieve payment details in DB
        try:
            existingPayment = PaymentDetails.objects.get(cardholderName=cardholderName, cardNumber=cardNumber, expiryDate=expiryDate, cardType=cardType)
        except PaymentDetails.DoesNotExist:
            return redirect("getPayment_Modify")

        #go to viewing page
        return redirect("viewBooking", payment_id = existingPayment.id)

    return render(request, "cust/enterPayment.html")

def viewBooking(request,payment_id):
    #get booking related to payment details
    try:
        booking_list = Booking.objects.filter(paymentRef=payment_id).values('showingRef', 'ticketQuantity', 'totalCost', 'paymentRef')
        # print(booking_list)
    except Booking.DoesNotExist:
        print("No bookings")
        return redirect("home")

    if request.method == "POST":
        #get booking to see the showing of
        selectedBooking = request.POST['selectedBooking']
        #go to showing page
        return redirect("viewShowing", selectedBooking)
    
    return render(request, "cust/viewBooking.html",
        {
            'booking_list': booking_list,
        })

def viewShowing(request, selectedBooking):
    #get showing of booking
    showing = Showings.objects.get(id=selectedBooking)
    #send showing to HTML page for viewing.
    return render(request, "cust/viewShowing.html",
        {
            'showing': showing,
        })

#VIEW WAS USED FOR POPULATING DB - NOT USED
def sampleData(request):
    # seats = [100, 125, 75, 90, 110]
    # for cap in seats:
    #     newScreen = Screen(capacity = cap)
    #     newScreen.save()

    # screens = Screen.objects.all()
    # filmShowings = [[datetime.date(2023, 4, 5), "Avatar", 13, 2.7, "Blue people fight against humans.", 0, screens[0]],
    # [datetime.date(2023, 4, 6), "Finding Nemo", 4, 1.66, "Fish searches for thier lost son!", 0, screens[1]],
    # [datetime.date(2023, 4, 4), "Toy Story", 12, 1.35, "The toys have come to life.", 0, screens[2]],
    # [datetime.date(2023, 4, 7), "The Matrix", 15, 2.26, "Mr Anderson plugs into the matrix to fight a war against powerful computers.", 0, screens[3]],
    # [datetime.date(2023, 4, 9), "Jurassic Park", 13, 2.11, "Dinosaurs are on the loose at a theme park.", 0, screens[4]],
    # ]
    # filmShowings = [[datetime.date(2023, 4, 5), "The Lion King", 4, 1.45, "Simba comes to reclaim thier throne.", 0, screens[4], '10:30:00'],
    # [datetime.date(2023, 4, 6), "Home Alone", 8, 1.71, "Kevin defends their home from invading thieves", 0, screens[3], '13:45:00'],
    # [datetime.date(2023, 4, 4), "Toy Story 2", 4, 1.58, "Woody needs to be rescued from a toy collector.", 0, screens[2], '11:15:00'],
    # [datetime.date(2023, 4, 7), "Frozen", 5, 1.8, "Two sisters living in a never-ending winter.", 0, screens[1], '14:00:00'],
    # [datetime.date(2023, 4, 9), "Shrek", 8, 1.5, "The ogre, Shrek, sets off to rescue Princess Fiona.", 0, screens[0], '16:25:00'],
    # ]
    # for show in filmShowings:
    #     newShow = Showings(showingDate=show[0],filmTitle=show[1],ageRating=show[2],filmDuration=show[3],trailerDescription=show[4],ticketsSold=show[5], screen=show[6], showingTime=show[7])
    #     newShow.save()

    #changing times for showings
    # times = ['12:00:00', '10:30:00', '13:15:00', '15:45:00', '14:10:00']
    # showings = Showings.objects.all()
    # for i in range(len(showings)):
    #     showings[i].showingTime = times[i]
    #     showings[i].save()
    return HttpResponse("DB")