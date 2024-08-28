import React from 'react';
import Header from './Header';
import Footer from './Footer';

function Contact() {
  return (
    <div>
      <Header />
      <div className="container mx-auto mt-24 p-8">
        <h1 className="text-4xl font-bold text-green-800 mb-8">Contact Us</h1>
        <p className="text-xl text-gray-700 mb-8">
          Have questions or suggestions? We'd love to hear from you!
        </p>
        {/* Add a contact form or contact information here */}
      </div>
      <Footer />
    </div>
  );
}

export default Contact;