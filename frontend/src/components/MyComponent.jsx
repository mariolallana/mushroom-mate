import * as React from "react";

function MyComponent(props) {
  return (
    <div className="flex flex-col items-stretch bg-white">
      <div className="flex overflow-hidden relative flex-col items-center px-5 pb-12 w-full min-h-[2196px] max-md:max-w-full">
        <img
          loading="lazy"
          srcSet="https://cdn.builder.io/api/v1/image/assets/TEMP/48d1e70610f6903edeb7a48ef947538c26a0e78ff9f6cc2f6d7f3a1e8a39ed8f?apiKey=f15ed31320e6455482803e44a3459736&width=100 100w, https://cdn.builder.io/api/v1/image/assets/TEMP/48d1e70610f6903edeb7a48ef947538c26a0e78ff9f6cc2f6d7f3a1e8a39ed8f?apiKey=f15ed31320e6455482803e44a3459736&width=200 200w, https://cdn.builder.io/api/v1/image/assets/TEMP/48d1e70610f6903edeb7a48ef947538c26a0e78ff9f6cc2f6d7f3a1e8a39ed8f?apiKey=f15ed31320e6455482803e44a3459736&width=400 400w, https://cdn.builder.io/api/v1/image/assets/TEMP/48d1e70610f6903edeb7a48ef947538c26a0e78ff9f6cc2f6d7f3a1e8a39ed8f?apiKey=f15ed31320e6455482803e44a3459736&width=800 800w, https://cdn.builder.io/api/v1/image/assets/TEMP/48d1e70610f6903edeb7a48ef947538c26a0e78ff9f6cc2f6d7f3a1e8a39ed8f?apiKey=f15ed31320e6455482803e44a3459736&width=1200 1200w, https://cdn.builder.io/api/v1/image/assets/TEMP/48d1e70610f6903edeb7a48ef947538c26a0e78ff9f6cc2f6d7f3a1e8a39ed8f?apiKey=f15ed31320e6455482803e44a3459736&width=1600 1600w, https://cdn.builder.io/api/v1/image/assets/TEMP/48d1e70610f6903edeb7a48ef947538c26a0e78ff9f6cc2f6d7f3a1e8a39ed8f?apiKey=f15ed31320e6455482803e44a3459736&width=2000 2000w, https://cdn.builder.io/api/v1/image/assets/TEMP/48d1e70610f6903edeb7a48ef947538c26a0e78ff9f6cc2f6d7f3a1e8a39ed8f?apiKey=f15ed31320e6455482803e44a3459736&"
          className="object-cover object-center absolute inset-0 size-full"
        />
        <div className="relative self-stretch px-20 w-full bg-green-800 bg-opacity-60 max-md:px-5 max-md:max-w-full">
          <div className="flex gap-5 max-md:flex-col max-md:gap-0 max-md:items-stretch">
            <div className="flex flex-col items-stretch w-[28%] max-md:ml-0 max-md:w-full">
              <img
                loading="lazy"
                srcSet="https://cdn.builder.io/api/v1/image/assets/TEMP/65abc810cd94bf89451dfc36c3a06c9e03690cb07a1fcbe528862127bd095365?apiKey=f15ed31320e6455482803e44a3459736&width=100 100w, https://cdn.builder.io/api/v1/image/assets/TEMP/65abc810cd94bf89451dfc36c3a06c9e03690cb07a1fcbe528862127bd095365?apiKey=f15ed31320e6455482803e44a3459736&width=200 200w, https://cdn.builder.io/api/v1/image/assets/TEMP/65abc810cd94bf89451dfc36c3a06c9e03690cb07a1fcbe528862127bd095365?apiKey=f15ed31320e6455482803e44a3459736&width=400 400w, https://cdn.builder.io/api/v1/image/assets/TEMP/65abc810cd94bf89451dfc36c3a06c9e03690cb07a1fcbe528862127bd095365?apiKey=f15ed31320e6455482803e44a3459736&width=800 800w, https://cdn.builder.io/api/v1/image/assets/TEMP/65abc810cd94bf89451dfc36c3a06c9e03690cb07a1fcbe528862127bd095365?apiKey=f15ed31320e6455482803e44a3459736&width=1200 1200w, https://cdn.builder.io/api/v1/image/assets/TEMP/65abc810cd94bf89451dfc36c3a06c9e03690cb07a1fcbe528862127bd095365?apiKey=f15ed31320e6455482803e44a3459736&width=1600 1600w, https://cdn.builder.io/api/v1/image/assets/TEMP/65abc810cd94bf89451dfc36c3a06c9e03690cb07a1fcbe528862127bd095365?apiKey=f15ed31320e6455482803e44a3459736&width=2000 2000w, https://cdn.builder.io/api/v1/image/assets/TEMP/65abc810cd94bf89451dfc36c3a06c9e03690cb07a1fcbe528862127bd095365?apiKey=f15ed31320e6455482803e44a3459736&"
                className="object-contain object-center shrink-0 max-w-full aspect-[0.65] w-[155px] max-md:mt-10"
              />
            </div>
            <div className="flex flex-col items-stretch ml-5 w-[72%] max-md:ml-0 max-md:w-full">
              <div className="relative self-stretch my-auto text-5xl font-bold text-center text-white max-md:mt-10 max-md:max-w-full max-md:text-4xl">
                MUSHROOM
                <br />
                MATE
              </div>
            </div>
          </div>
        </div>
        <div className="relative mt-28 text-5xl text-center text-yellow-900 max-md:mt-10 max-md:max-w-full">
          Welcome to MushroomMate
        </div>
        <div className="relative mt-16 text-xl text-center text-yellow-900 max-md:mt-10 max-md:max-w-full">
          Explore the wonders of mushroom foraging in mountainous and forested
          areas
        </div>
        <div className="flex relative gap-5 justify-between items-stretch mt-11 max-w-full w-[513px] max-md:flex-wrap max-md:mt-10">
          <div className="justify-center items-stretch px-6 py-3.5 text-xl font-bold text-center text-white bg-green-800 rounded shadow-sm max-md:px-5">
            Login
          </div>
          <div className="justify-center items-stretch px-10 py-4 text-xl font-bold text-center text-white bg-green-800 rounded shadow-sm max-md:px-5">
            Register
          </div>
        </div>
        <div className="flex relative flex-col justify-center items-center self-stretch px-16 py-12 mt-24 w-full bg-green-500 bg-opacity-90 max-md:px-5 max-md:mt-10 max-md:max-w-full">
          <div className="flex flex-col items-stretch mt-4 w-full max-w-[891px] max-md:max-w-full">
            <div className="self-center text-4xl font-bold text-center text-white max-md:max-w-full">
              Discover the Magic of Mushroom Foraging
            </div>
            <div className="mt-8 max-md:max-w-full">
              <div className="flex gap-5 max-md:flex-col max-md:gap-0 max-md:items-stretch">
                <div className="flex flex-col items-stretch w-[34%] max-md:ml-0 max-md:w-full">
                  <div className="flex flex-col grow items-center mt-2.5 text-center text-white max-md:mt-10">
                    <img
                      loading="lazy"
                      srcSet="https://cdn.builder.io/api/v1/image/assets/TEMP/7f1eb1e9b2496307ecd3c8943d585857a7e6faf5c4c8ded1e255405499a4252b?apiKey=f15ed31320e6455482803e44a3459736&width=100 100w, https://cdn.builder.io/api/v1/image/assets/TEMP/7f1eb1e9b2496307ecd3c8943d585857a7e6faf5c4c8ded1e255405499a4252b?apiKey=f15ed31320e6455482803e44a3459736&width=200 200w, https://cdn.builder.io/api/v1/image/assets/TEMP/7f1eb1e9b2496307ecd3c8943d585857a7e6faf5c4c8ded1e255405499a4252b?apiKey=f15ed31320e6455482803e44a3459736&width=400 400w, https://cdn.builder.io/api/v1/image/assets/TEMP/7f1eb1e9b2496307ecd3c8943d585857a7e6faf5c4c8ded1e255405499a4252b?apiKey=f15ed31320e6455482803e44a3459736&width=800 800w, https://cdn.builder.io/api/v1/image/assets/TEMP/7f1eb1e9b2496307ecd3c8943d585857a7e6faf5c4c8ded1e255405499a4252b?apiKey=f15ed31320e6455482803e44a3459736&width=1200 1200w, https://cdn.builder.io/api/v1/image/assets/TEMP/7f1eb1e9b2496307ecd3c8943d585857a7e6faf5c4c8ded1e255405499a4252b?apiKey=f15ed31320e6455482803e44a3459736&width=1600 1600w, https://cdn.builder.io/api/v1/image/assets/TEMP/7f1eb1e9b2496307ecd3c8943d585857a7e6faf5c4c8ded1e255405499a4252b?apiKey=f15ed31320e6455482803e44a3459736&width=2000 2000w, https://cdn.builder.io/api/v1/image/assets/TEMP/7f1eb1e9b2496307ecd3c8943d585857a7e6faf5c4c8ded1e255405499a4252b?apiKey=f15ed31320e6455482803e44a3459736&"
                      className="object-contain object-center w-32 max-w-full aspect-[1.06]"
                    />
                    <div className="mt-9 text-2xl font-bold">
                      Explore Breathtaking Forests
                    </div>
                    <div className="self-stretch mt-7 text-lg">
                      Immerse yourself in the beauty of nature as you traverse
                      through lush green forests
                    </div>
                  </div>
                </div>
                <div className="flex flex-col items-stretch ml-5 w-[38%] max-md:ml-0 max-md:w-full">
                  <div className="flex flex-col items-center text-center text-white max-md:mt-10">
                    <img
                      loading="lazy"
                      srcSet="https://cdn.builder.io/api/v1/image/assets/TEMP/e50b678d6674509eca529258997e3624f3f9f851470ecb54e64d340c44cf74c5?apiKey=f15ed31320e6455482803e44a3459736&width=100 100w, https://cdn.builder.io/api/v1/image/assets/TEMP/e50b678d6674509eca529258997e3624f3f9f851470ecb54e64d340c44cf74c5?apiKey=f15ed31320e6455482803e44a3459736&width=200 200w, https://cdn.builder.io/api/v1/image/assets/TEMP/e50b678d6674509eca529258997e3624f3f9f851470ecb54e64d340c44cf74c5?apiKey=f15ed31320e6455482803e44a3459736&width=400 400w, https://cdn.builder.io/api/v1/image/assets/TEMP/e50b678d6674509eca529258997e3624f3f9f851470ecb54e64d340c44cf74c5?apiKey=f15ed31320e6455482803e44a3459736&width=800 800w, https://cdn.builder.io/api/v1/image/assets/TEMP/e50b678d6674509eca529258997e3624f3f9f851470ecb54e64d340c44cf74c5?apiKey=f15ed31320e6455482803e44a3459736&width=1200 1200w, https://cdn.builder.io/api/v1/image/assets/TEMP/e50b678d6674509eca529258997e3624f3f9f851470ecb54e64d340c44cf74c5?apiKey=f15ed31320e6455482803e44a3459736&width=1600 1600w, https://cdn.builder.io/api/v1/image/assets/TEMP/e50b678d6674509eca529258997e3624f3f9f851470ecb54e64d340c44cf74c5?apiKey=f15ed31320e6455482803e44a3459736&width=2000 2000w, https://cdn.builder.io/api/v1/image/assets/TEMP/e50b678d6674509eca529258997e3624f3f9f851470ecb54e64d340c44cf74c5?apiKey=f15ed31320e6455482803e44a3459736&"
                      className="object-contain object-center aspect-[0.61] w-[85px]"
                    />
                    <div className="mt-7 text-2xl font-bold">
                      Find Exquisite Mushrooms
                    </div>
                    <div className="self-stretch mt-7 text-lg">
                      Discover a variety of mushrooms, from the common to the
                      rare and exotic
                    </div>
                  </div>
                </div>
                <div className="flex flex-col items-stretch ml-5 w-[28%] max-md:ml-0 max-md:w-full">
                  <div className="flex flex-col items-stretch text-center text-white max-md:mt-10">
                    <img
                      loading="lazy"
                      srcSet="https://cdn.builder.io/api/v1/image/assets/TEMP/fb007dfe4bbc5c767675bad1baa60b088c93ebf8a9bce9740244c9b187f85e0a?apiKey=f15ed31320e6455482803e44a3459736&width=100 100w, https://cdn.builder.io/api/v1/image/assets/TEMP/fb007dfe4bbc5c767675bad1baa60b088c93ebf8a9bce9740244c9b187f85e0a?apiKey=f15ed31320e6455482803e44a3459736&width=200 200w, https://cdn.builder.io/api/v1/image/assets/TEMP/fb007dfe4bbc5c767675bad1baa60b088c93ebf8a9bce9740244c9b187f85e0a?apiKey=f15ed31320e6455482803e44a3459736&width=400 400w, https://cdn.builder.io/api/v1/image/assets/TEMP/fb007dfe4bbc5c767675bad1baa60b088c93ebf8a9bce9740244c9b187f85e0a?apiKey=f15ed31320e6455482803e44a3459736&width=800 800w, https://cdn.builder.io/api/v1/image/assets/TEMP/fb007dfe4bbc5c767675bad1baa60b088c93ebf8a9bce9740244c9b187f85e0a?apiKey=f15ed31320e6455482803e44a3459736&width=1200 1200w, https://cdn.builder.io/api/v1/image/assets/TEMP/fb007dfe4bbc5c767675bad1baa60b088c93ebf8a9bce9740244c9b187f85e0a?apiKey=f15ed31320e6455482803e44a3459736&width=1600 1600w, https://cdn.builder.io/api/v1/image/assets/TEMP/fb007dfe4bbc5c767675bad1baa60b088c93ebf8a9bce9740244c9b187f85e0a?apiKey=f15ed31320e6455482803e44a3459736&width=2000 2000w, https://cdn.builder.io/api/v1/image/assets/TEMP/fb007dfe4bbc5c767675bad1baa60b088c93ebf8a9bce9740244c9b187f85e0a?apiKey=f15ed31320e6455482803e44a3459736&"
                      className="object-contain object-center self-center max-w-full aspect-square w-[157px]"
                    />
                    <div className="mt-2 text-2xl font-bold">
                      Conquer Majestic Mountains
                    </div>
                    <div className="mt-6 text-lg">
                      Embark on a thrilling uphill journey to uncover hidden
                      mushroom treasures
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
        <img
          loading="lazy"
          srcSet="https://cdn.builder.io/api/v1/image/assets/TEMP/2b2064b376870d9b9b40f9aeebb4d5a9c3e57419c085e4f2c34fd3d258397093?apiKey=f15ed31320e6455482803e44a3459736&width=100 100w, https://cdn.builder.io/api/v1/image/assets/TEMP/2b2064b376870d9b9b40f9aeebb4d5a9c3e57419c085e4f2c34fd3d258397093?apiKey=f15ed31320e6455482803e44a3459736&width=200 200w, https://cdn.builder.io/api/v1/image/assets/TEMP/2b2064b376870d9b9b40f9aeebb4d5a9c3e57419c085e4f2c34fd3d258397093?apiKey=f15ed31320e6455482803e44a3459736&width=400 400w, https://cdn.builder.io/api/v1/image/assets/TEMP/2b2064b376870d9b9b40f9aeebb4d5a9c3e57419c085e4f2c34fd3d258397093?apiKey=f15ed31320e6455482803e44a3459736&width=800 800w, https://cdn.builder.io/api/v1/image/assets/TEMP/2b2064b376870d9b9b40f9aeebb4d5a9c3e57419c085e4f2c34fd3d258397093?apiKey=f15ed31320e6455482803e44a3459736&width=1200 1200w, https://cdn.builder.io/api/v1/image/assets/TEMP/2b2064b376870d9b9b40f9aeebb4d5a9c3e57419c085e4f2c34fd3d258397093?apiKey=f15ed31320e6455482803e44a3459736&width=1600 1600w, https://cdn.builder.io/api/v1/image/assets/TEMP/2b2064b376870d9b9b40f9aeebb4d5a9c3e57419c085e4f2c34fd3d258397093?apiKey=f15ed31320e6455482803e44a3459736&width=2000 2000w, https://cdn.builder.io/api/v1/image/assets/TEMP/2b2064b376870d9b9b40f9aeebb4d5a9c3e57419c085e4f2c34fd3d258397093?apiKey=f15ed31320e6455482803e44a3459736&"
          className="object-contain object-center mt-28 w-full aspect-[1.25] max-w-[831px] max-md:mt-10 max-md:max-w-full"
        />
        <div className="relative mt-20 text-4xl text-center text-yellow-900 max-md:mt-10 max-md:max-w-full">
          Explore Mushroom Hotspots
        </div>
        <div className="relative mt-12 text-xl text-center text-yellow-900 max-md:mt-10 max-md:max-w-full">
          Discover locations with a high likelihood of finding mushrooms
        </div>
        <div className="relative justify-center items-stretch px-12 py-4 mt-8 mb-9 text-xl text-center text-white whitespace-nowrap bg-green-800 rounded max-md:px-5">
          Find Locations
        </div>
      </div>
      <div className="flex flex-col justify-center items-center px-16 py-12 w-full bg-green-400 max-md:px-5 max-md:max-w-full">
        <div className="flex flex-col items-stretch mt-9 mb-6 w-full max-w-[942px] max-md:max-w-full">
          <div className="self-center text-4xl font-bold text-center text-white max-md:max-w-full">
            Join the Mushroom Foraging Community
          </div>
          <div className="mt-11 max-md:mt-10 max-md:max-w-full">
            <div className="flex gap-5 max-md:flex-col max-md:gap-0 max-md:items-stretch">
              <div className="flex flex-col items-stretch w-[31%] max-md:ml-0 max-md:w-full">
                <div className="flex flex-col grow items-stretch text-center text-white max-md:mt-10">
                  <div className="text-2xl font-bold">
                    Connect with Like-minded Enthusiasts
                  </div>
                  <div className="mt-11 text-lg max-md:mt-10">
                    Share your experiences, tips, and findings with a community
                    of passionate mushroom foragers
                  </div>
                </div>
              </div>
              <div className="flex flex-col items-stretch ml-5 w-[35%] max-md:ml-0 max-md:w-full">
                <div className="flex flex-col items-stretch text-center text-white max-md:mt-10">
                  <div className="text-2xl font-bold whitespace-nowrap">
                    Discover Expert Expertise
                  </div>
                  <div className="mt-10 text-lg">
                    Learn from experienced foragers and gain valuable insights
                    into mushroom foraging techniques
                  </div>
                </div>
              </div>
              <div className="flex flex-col items-stretch ml-5 w-[34%] max-md:ml-0 max-md:w-full">
                <div className="flex flex-col items-stretch text-center text-white max-md:mt-10">
                  <div className="self-center text-2xl font-bold whitespace-nowrap">
                    Stay Updated
                  </div>
                  <div className="mt-10 text-lg">
                    Get the latest news and updates on mushroom foraging events,
                    workshops, and gatherings
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default MyComponent;

