import React from "react";
import { View, Text, Button, StyleSheet } from "react-native";
import LottieLoader from "../components/LottieLoader";
import { router } from "expo-router";

export default function OnboardingScreen() {
  return (
    <View style={styles.container}>
      <LottieLoader source={require("../assets/lottie/onboarding.json")} />
      <Text style={styles.title}>Welcome to Mindful App!</Text>
      <Text style={styles.text}>
        Your journey to better mental health starts here. Let’s walk you through
        some features.
      </Text>
      <Button title="Get Started" onPress={() => router.replace("/")} />
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: "center",
    alignItems: "center",
    padding: 20,
  },
  title: { fontSize: 24, fontWeight: "bold", marginBottom: 20 },
  text: { fontSize: 16, textAlign: "center", marginBottom: 40 },
});
