from django.db import models


class Image(models.Model):
    '''
    Model to store bookmarked images
    '''

    user = models.ForeignKey(
        "account.Profile",
        related_name="images_created",
        on_delete=models.CASCADE
    )
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, blank=True)
    url = models.URLField(max_length=2000)
    image = models.ImageField(upload_to="images/%Y/%m/%d/")
    description = models.TextField(blank=True)
    users_like = models.ManyToManyField(
        "account.Profile",
        related_name="images_liked",
        blank=True
    )
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        # Define database index in descending order for created field
        indexes = [
            models.Index(fields=["-created"]),
        ]
        # Telling django to sort the results by the created field by default
        ordering = ["-created"]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        '''
        Add slug from title if slug doesn't have a value,
        before saving the object
        '''
        from django.utils.text import slugify
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        '''Absolute url for each image'''
        from django.urls import reverse
        return reverse("image:detail", args=[self.id, self.slug])
