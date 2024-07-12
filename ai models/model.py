import os
import cv2
import numpy as np
import tensorflow as tf
from tensorflow_examples.models.pix2pix import pix2pix
import datetime
import matplotlib.pyplot as plt

def load_images(folder):
    images = []
    for filename in sorted(os.listdir(folder), key=lambda x: int(os.path.splitext(x)[0])):
        print(filename)
        img = cv2.imread(os.path.join(folder, filename))
        if img is not None:
            img = cv2.resize(img, (256, 256))
            img = (img / 127.5) - 1  # Normalize to [-1, 1]
            images.append(img)
    return np.array(images, dtype=np.float32)

blank_images = load_images(r"C:\Users\prabh\Downloads\pairs\blanks")
furnished_images = load_images(r"C:\Users\prabh\Downloads\pairs\furnishes")

# Verify shapes
print(blank_images.shape, furnished_images.shape)

# Create TensorFlow dataset
BUFFER_SIZE = 400
BATCH_SIZE = 1

dataset = tf.data.Dataset.from_tensor_slices((blank_images, furnished_images))
dataset = dataset.shuffle(BUFFER_SIZE).batch(BATCH_SIZE)

OUTPUT_CHANNELS = 3

# Create generator and discriminator
generator = pix2pix.unet_generator(OUTPUT_CHANNELS, norm_type='batchnorm')
discriminator = pix2pix.discriminator(norm_type='batchnorm', target=True)

# Define loss functions
loss_object = tf.keras.losses.BinaryCrossentropy(from_logits=True)

def generator_loss(disc_generated_output, gen_output, target):
    target = tf.cast(target, tf.float32)
    gan_loss = loss_object(tf.ones_like(disc_generated_output), disc_generated_output)
    l1_loss = tf.reduce_mean(tf.abs(target - gen_output))
    total_gen_loss = gan_loss + (100 * l1_loss)
    return total_gen_loss

def discriminator_loss(disc_real_output, disc_generated_output):
    real_loss = loss_object(tf.ones_like(disc_real_output), disc_real_output)
    generated_loss = loss_object(tf.zeros_like(disc_generated_output), disc_generated_output)
    total_disc_loss = real_loss + generated_loss
    return total_disc_loss

# Define optimizers
generator_optimizer = tf.keras.optimizers.Adam(2e-4, beta_1=0.5)
discriminator_optimizer = tf.keras.optimizers.Adam(2e-4, beta_1=0.5)

@tf.function
def train_step(input_image, target, epoch):
    target = tf.cast(target, tf.float32)
    with tf.GradientTape() as gen_tape, tf.GradientTape() as disc_tape:
        generated_image = generator(input_image, training=True)

        disc_real_output = discriminator([input_image, target], training=True)
        disc_generated_output = discriminator([input_image, generated_image], training=True)

        gen_loss = generator_loss(disc_generated_output, generated_image, target)
        disc_loss = discriminator_loss(disc_real_output, disc_generated_output)

    generator_gradients = gen_tape.gradient(gen_loss, generator.trainable_variables)
    discriminator_gradients = disc_tape.gradient(disc_loss, discriminator.trainable_variables)

    generator_optimizer.apply_gradients(zip(generator_gradients, generator.trainable_variables))
    discriminator_optimizer.apply_gradients(zip(discriminator_gradients, discriminator.trainable_variables))

    return gen_loss, disc_loss

# Training loop
EPOCHS = 1000
for epoch in range(EPOCHS):
    start = datetime.datetime.now()
    for input_image, target in dataset:
        gen_loss, disc_loss = train_step(input_image, target, epoch)
    print(f'Epoch {epoch+1}, Generator Loss: {gen_loss}, Discriminator Loss: {disc_loss}, Time: {datetime.datetime.now() - start}')

def preprocess_image(image_path):
    img = cv2.imread(image_path)
    img = cv2.resize(img, (256, 256))  # Resize to the expected input size
    img = (img / 127.5) - 1  # Normalize to [-1, 1]
    img = np.expand_dims(img, axis=0)  # Add batch dimension
    return img

def postprocess_image(image):
    image = (image + 1) * 127.5  # De-normalize to [0, 255]
    image = np.array(image, dtype=np.uint8)  # Convert to uint8
    return image

blank_image_path = r"C:\Users\prabh\Downloads\pairs\stock-photo-modern-bright-interiors-3d-rendering-illustration.jpeg"
blank_image = preprocess_image(blank_image_path)

# Generate the furnished image
furnished_image = generator(blank_image, training=False)

# Post-process the generated image
furnished_image = postprocess_image(furnished_image[0])  # Remove batch dimension

# Save the result
output_path = r"C:\Users\prabh\Downloads\pairs\d.jpeg"
cv2.imwrite(output_path, furnished_image)

# Display the result
plt.imshow(cv2.cvtColor(furnished_image, cv2.COLOR_BGR2RGB))
plt.title('Furnished Image')
plt.axis('off')
plt.show()
