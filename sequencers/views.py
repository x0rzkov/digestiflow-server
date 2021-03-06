"""The views for the sequencers app."""

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.shortcuts import reverse
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView
from projectroles.plugins import get_backend_api
from projectroles.views import LoggedInPermissionMixin, ProjectContextMixin

from digestiflow.utils import model_to_dict, ProjectPermissionMixin
from .forms import SequencingMachineForm
from .models import SequencingMachine


class SequencingMachineListView(
    LoginRequiredMixin,
    LoggedInPermissionMixin,
    ProjectPermissionMixin,
    ProjectContextMixin,
    ListView,
):
    """Display list of all SequencingMachine records"""

    template_name = "sequencers/sequencer_list.html"
    permission_required = "sequencers.view_sequencingmachine"

    model = SequencingMachine
    paginate_by = 10

    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .filter(project__sodar_uuid=self.kwargs["project"])
            .prefetch_related("flowcell_set", "project")
        )


class SequencingMachineDetailView(
    LoginRequiredMixin,
    LoggedInPermissionMixin,
    ProjectPermissionMixin,
    ProjectContextMixin,
    DetailView,
):
    """Display detail of SequencingMachine records"""

    template_name = "sequencers/sequencer_detail.html"
    permission_required = "sequencers.view_sequencingmachine"

    model = SequencingMachine

    slug_url_kwarg = "sequencer"
    slug_field = "sodar_uuid"


class SequencingMachineCreateView(
    LoginRequiredMixin,
    LoggedInPermissionMixin,
    ProjectPermissionMixin,
    ProjectContextMixin,
    CreateView,
):
    """Display list of all SequencingMachine records"""

    template_name = "sequencers/sequencer_create.html"
    permission_required = "sequencers.add_sequencingmachine"

    model = SequencingMachine
    form_class = SequencingMachineForm

    @transaction.atomic
    def form_valid(self, form):
        """Automatically set the project property."""
        # Create the sequencing machine.
        form.instance.project = self.get_project(self.request, self.kwargs)
        result = super().form_valid(form)
        # Register event with timeline.
        timeline = get_backend_api("timeline_backend")
        if timeline:
            tl_event = timeline.add_event(
                project=self.get_project(self.request, self.kwargs),
                app_name="sequencers",
                user=self.request.user,
                event_name="sequencer_create",
                description="create sequencer {sequencer}: {extra-sequencer_dict}",
                status_type="OK",
                extra_data={"sequencer_dict": model_to_dict(self.object)},
            )
            tl_event.add_object(obj=self.object, label="sequencer", name=self.object.vendor_id)
        return result


class SequencingMachineUpdateView(
    LoginRequiredMixin,
    LoggedInPermissionMixin,
    ProjectPermissionMixin,
    ProjectContextMixin,
    UpdateView,
):
    """Updating of SequencingMachine records"""

    template_name = "sequencers/sequencer_update.html"
    permission_required = "sequencers.change_sequencingmachine"

    model = SequencingMachine
    form_class = SequencingMachineForm

    slug_url_kwarg = "sequencer"
    slug_field = "sodar_uuid"

    @transaction.atomic
    def form_valid(self, form):
        # Update sequencing machine record.
        result = super().form_valid(form)
        # Register event with timeline.
        timeline = get_backend_api("timeline_backend")
        if timeline:
            tl_event = timeline.add_event(
                project=self.get_project(self.request, self.kwargs),
                app_name="sequencers",
                user=self.request.user,
                event_name="sequencer_update",
                description="update sequencer {sequencer}: {extra-sequencer_dict}",
                status_type="OK",
                extra_data={"sequencer_dict": model_to_dict(self.object)},
            )
            tl_event.add_object(obj=self.object, label="sequencer", name=self.object.vendor_id)
        return result


class SequencingMachineDeleteView(
    LoginRequiredMixin,
    LoggedInPermissionMixin,
    ProjectPermissionMixin,
    ProjectContextMixin,
    DeleteView,
):
    """Deletion of SequencingMachine records"""

    template_name = "sequencers/sequencer_confirm_delete.html"
    permission_required = "sequencers.delete_sequencingmachine"

    model = SequencingMachine

    slug_url_kwarg = "sequencer"
    slug_field = "sodar_uuid"

    @transaction.atomic
    def delete(self, *args, **kwargs):
        # Delete sequencing machine record.
        result = super().delete(*args, **kwargs)
        # Register event with timeline.
        timeline = get_backend_api("timeline_backend")
        if timeline:
            tl_event = timeline.add_event(
                project=self.get_project(self.request, self.kwargs),
                app_name="sequencers",
                user=self.request.user,
                event_name="sequencer_delete",
                description="delete sequencer {sequencer}: {extra-sequencer_dict}",
                status_type="OK",
                extra_data={"sequencer_dict": model_to_dict(self.object)},
            )
            tl_event.add_object(obj=self.object, label="sequencer", name=self.object.vendor_id)
        return result

    def get_success_url(self):
        return reverse(
            "sequencers:sequencer-list",
            kwargs={"project": self.get_project(self.request, self.kwargs).sodar_uuid},
        )
