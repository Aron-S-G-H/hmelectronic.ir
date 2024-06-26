from django.shortcuts import render
from django.views.generic import View
from .forms import ContactUsForm
from django.http import JsonResponse
from .tasks import send_confirm_email_admins


class ContactUsView(View):
    def get(self, request):
        form = ContactUsForm()
        return render(request, 'contact_app/contact.html', {'form': form})

    def post(self, request):
        if request.user.is_authenticated:
            form = ContactUsForm(request.POST)
            if form.is_valid():
                instance = form.save(commit=False)
                instance.user = request.user
                instance.save()
                send_confirm_email_admins.apply_async(
                    (instance.created_at,),
                    retry=False,
                    ignore_result=True,
                    expires=30
                )
                return JsonResponse({'status': 200})
            else:
                return JsonResponse({'status': 400})
        else:
            return JsonResponse({'status': 401})
